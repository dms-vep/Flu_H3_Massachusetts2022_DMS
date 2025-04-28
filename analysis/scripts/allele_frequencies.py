import argparse
import json
import os
import pandas as pd
import numpy as np
from Bio import Phylo
from collections import defaultdict
from datetime import datetime, timedelta
import re

def fractional_year_to_date(frac_year):
    """Convert a fractional year (e.g., 2024.5) to a date."""
    year = int(frac_year)
    days = (frac_year - year) * 365
    date = datetime(year, 1, 1) + timedelta(days=days)
    return date


def propagate_mutations(
    clade, 
    mutations_df, 
    curr_alleles, 
    tip_alleles
):
    """
    Get the genotype at each tip of a phylogenetic tree by propagating mutations 
    down branches so each node inherits mutations from its parent.

    Parameters
    ----------
    clade : Starting node for propagating, typically 'tree.root'.
    mutations_df : pd.DataFrame with two columns
        - 'name': Clade names corresponding to internal nodes in the tree.
        - 'mutations': String representation of mutations in the format 
          "{'HA1': ['A123T', 'G456D'], 'HA2': ['V89I']}".
    curr_alleles : dict of allele states at each site before propagation.
    tip_alleles : dict of final allele states at each tip.
    """
    curr_alleles = {region: alleles.copy() for region, alleles in curr_alleles.items()}
    clade_mutations = mutations_df.query("name == @clade.name")['mutations']

    # update curr_alleles with clade mutations
    if not clade_mutations.empty:
        clade_mutations_dict = eval(
            clade_mutations.values[0]
        ) # convert string dict -> literal dict
        
        for region in ['HA1', 'HA2']:
            if region in clade_mutations_dict:
                for mutation in clade_mutations_dict[region]:
                    site = int(re.search(r'\d+', mutation).group())
                    allele = mutation[-1] # ex. 'T' in 'A123T' 
                    curr_alleles.setdefault(region, {})[site] = allele

    # save final alleles if tip is terminal, otherwise propagate
    if clade.is_terminal():
        tip_alleles[clade.name] = curr_alleles
    else:
        for child in clade.clades:
            propagate_mutations(child, mutations_df, curr_alleles, tip_alleles)


def main(
    tree_file, 
    mutations_file, 
    frequencies_file, 
    main_json_file, 
    fix_cutoff, 
    output_frequencies_csv, 
    output_phenotypes_csv, 
    root_sequence_file=None
):
    # Load input files
    tree = Phylo.read(tree_file, "newick")
    mutations_df = pd.read_csv(mutations_file, sep='\t')

    with open(frequencies_file) as f:
        frequencies = json.load(f)

    with open(main_json_file) as f:
        main = json.load(f)

    # These are the reference dates eg. '1968.4167', '2021.4167'
    pivots = frequencies["pivots"]

    # Specify an external root sequence
    external_root_sequence = None
    if root_sequence_file:
        with open(root_sequence_file) as f:
            external_root_sequence = json.load(f)
        
        if external_root_sequence["name"] != tree.root.name:
            raise ValueError("Provided root sequence != tree root node.")

    # Extract root sequences
    if external_root_sequence:
        root_sequence_ha1 = external_root_sequence['HA1']
        root_sequence_ha2 = external_root_sequence['HA2']
    else:
        root_sequence_ha1 = main['root_sequence']['HA1']
        root_sequence_ha2 = main['root_sequence']['HA2']

    # Initialize allele states based on root sequence
    tip_alleles = defaultdict(lambda: defaultdict(dict))
    for i, aa in enumerate(root_sequence_ha1, start=1):
        tip_alleles['root']['HA1'][i] = aa
    for i, aa in enumerate(root_sequence_ha2, start=1):
        tip_alleles['root']['HA2'][i] = aa

    # Propagate mutations down the tree
    propagate_mutations(tree.root, mutations_df, tip_alleles['root'], tip_alleles)

    # Calculate allele frequencies
    allele_frequencies = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    )

    # Sum frequency of alleles at each timestamp
    for tip, regions in tip_alleles.items():
        if tip in frequencies:
            tip_frequencies = frequencies[tip]["frequencies"]
            for region, states in regions.items():
                for site, allele in states.items():
                    for i, freq in enumerate(tip_frequencies):
                        timestamp = pivots[i]
                        allele_frequencies[timestamp][region][site][allele] += freq

    # Normalize frequencies to be between 0 and 1
    for timestamp, regions in allele_frequencies.items():
        for region, states in regions.items():
            for site, alleles in states.items():
                total_frequency = sum(alleles.values())
                if total_frequency > 0:
                    for allele in alleles:
                        alleles[allele] /= total_frequency


    frequency_data = []
    for timestamp, regions in allele_frequencies.items():
        for region, states in regions.items():
            for site, alleles in states.items():
                for allele, freq in alleles.items():
                    frequency_data.append({
                        "timepoint": timestamp,
                        "HA_region": region,
                        "HA_site": site,
                        "allele": allele,
                        "frequency": freq
                    })

    # Create the DataFrame
    frequency_df = pd.DataFrame(frequency_data).assign(
        site=lambda x: np.where(x["HA_region"] == "HA1", x["HA_site"], x["HA_site"] + 329),
        date=lambda x: x['timepoint'].apply(fractional_year_to_date)
    ).sort_values(by=["site"]).reset_index(drop=True)

    # Save to frequencies csv
    frequency_df.to_csv(output_frequencies_csv, index=False)
    print(f"frequencies csv file successfully saved to {output_frequencies_csv}")

    # Integrate phenotype measurements and frequencies
    phenotypes = pd.read_csv(
        '../../results/summaries/Phenotypes.csv'
    ).drop(columns=['sera escape'])

    frequency_df = frequency_df.assign(
        is_fixed=lambda df: df['frequency'] >= fix_cutoff,
        most_recent_fix_date=lambda df: df.groupby(['site', 'allele'])['date'].transform(
            lambda dates: dates.where(df['frequency'] >= fix_cutoff).max()
        ),
        most_recent_fix_frequency=lambda df: df.apply(
            lambda row: row['frequency'] if row['date'] == row['most_recent_fix_date'] else pd.NA,
            axis=1
        ).groupby([df['site'], df['allele']]).transform('max'),
        max_frequency=lambda df: df.groupby(["site", "allele"])['frequency'].transform("max"),
        fix_frequency_cutoff=fix_cutoff
    )

    freqs_and_phenotypes = pd.merge(
        phenotypes,
        frequency_df[[
            'site', 'allele', 'max_frequency', 'fix_frequency_cutoff', 'most_recent_fix_date', 'most_recent_fix_frequency'
        ]].drop_duplicates(),
        left_on=['site', 'mutant'],
        right_on=['site', 'allele'],
        how='left'
    )

    # Save to phenotypes csv
    freqs_and_phenotypes.to_csv(output_phenotypes_csv, index=False)
    print(f"phenotypes csv file successfully saved to {output_phenotypes_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process phylogenetic data and output allele frequencies.")
    parser.add_argument("--tree_file", type=str, help="Path to the Newick tree file.")
    parser.add_argument("--mutations_file", type=str, help="Path to the TSV file containing mutations.")
    parser.add_argument("--frequencies_file", type=str, help="Path to the JSON file with frequency data.")
    parser.add_argument("--main_json_file", type=str, help="Path to the main JSON file with tree.")
    parser.add_argument("--fix_cutoff", type=float, help="Cutoff for whether or not allele is considered fixed.")
    parser.add_argument("--output_frequencies_csv", type=str, help="Path to save the output frequencies CSV file.")
    parser.add_argument("--output_phenotypes_csv", type=str, help="Path to save the output phenotypes CSV file.")
    parser.add_argument("--root_sequence_file", type=str, help="Path to JSON file with root sequences (optional).", default=None)

    args = parser.parse_args()
    main(
        args.tree_file, 
        args.mutations_file, 
        args.frequencies_file, 
        args.main_json_file, 
        args.fix_cutoff,
        args.output_frequencies_csv, 
        args.output_phenotypes_csv, 
        args.root_sequence_file
    )