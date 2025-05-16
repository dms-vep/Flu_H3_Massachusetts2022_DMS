"""writes .defattr for quantitively visualizing mean effects of each site on cell entry and stability."""

import pandas as pd
from Bio.PDB import PDBParser

def parse_chain_sites(pdb_path):
    """
    Parses a PDB file to extract site numbers for each chain.
    Adjusts site numbers for chains B, D, and F by adding 329.
    This function assumes the PDB:
        - Contains chains A-F, where A,C,E are HA1 and B,D,F are HA2.
        - Follows H3 numbering convention.

    Parameters:
        pdb_path (str): Path to the PDB file.
    
    Returns:
        dict: A dictionary with chain IDs as keys and a list of site numbers as values.
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)
    chain_sites = {}

    for model in structure:
        for chain in model:
            chain_id = chain.id
            # Extract residue site numbers
            sites = [residue.id[1] for residue in chain if residue.id[0] == " "]
            # Adjust sites for specific chains
            if chain_id in {"B", "D", "F"}:
                sites = [site + 329 for site in sites]
            chain_sites[chain_id] = sites

    return chain_sites

def aggregate_mean(infile, name, outfile, chain_mapping):
    df = pd.read_csv(infile)

    # Calculate the mean at each site
    if name == "entry":
        tmp_df = df.query(
            'mutant != "*" and mutant != wildtype'
        ).groupby('site')['effect'].mean().reset_index()
    elif name == "stability":
        tmp_df = df.query(
            '`MDCKSIAT1 cell entry` >= -3 and wildtype != mutant'
        ).groupby('site')['pH stability'].mean().reset_index().fillna(0)

    # Ensure site is integer
    tmp_df['site'] = tmp_df['site'].astype(int)

    # Write the output file
    with open(outfile, 'w') as f:
        # Write header lines
        f.write(f'attribute: {name}\n')
        f.write('match mode: 1-to-1\n')
        f.write('recipient: residues\n')
        
        # These are column names in dataframe that match phenotype
        effect = {
            'entry': 'effect', 
            'stability': 'pH stability'
        }

        # Write the formatted data for each chain
        for chain_id, chain_sites in chain_mapping.items():
            for site in chain_sites:
                residue = site if site < 330 else (site - 329)
                effect_value = tmp_df.loc[
                    tmp_df['site'] == site, effect[name]
                ].values
                effect_value = effect_value[0] if len(effect_value) > 0 else 0
                f.write(f'\t/{chain_id}:{residue}\t{effect_value:.6f}\n')

# Define the chain mappings

#4O5N
chain_mapping_4o5n = parse_chain_sites('pdbs/4o5n.pdb')
# 6Y5H
state_I_chain_mapping = parse_chain_sites('pdbs/6y5h.pdb1')
# 6Y5K
state_IV_chain_mapping = parse_chain_sites('pdbs/6y5k.pdb1')
# 1HTM
state_V_chain_mapping = parse_chain_sites('pdbs/1htm.pdb1')

# Takes input .csv and exports .defattr.
aggregate_mean(
    '../../results/func_effects/averages/MDCKSIAT1_entry_func_effects.csv',
    'entry',
    'cell_entry/cell_entry_mean.defattr',
    chain_mapping_4o5n,
)

aggregate_mean(
    '../../results/summaries/Phenotypes.csv',
    'stability',
    'stability/stability_mean_stateI.defattr',
    state_I_chain_mapping,
)

aggregate_mean(
    '../../results/summaries/Phenotypes.csv',
    'stability',
    'stability/stability_mean_stateIV.defattr',
    state_IV_chain_mapping
)

aggregate_mean(
    '../../results/summaries/Phenotypes.csv',
    'stability',
    'stability/stability_mean_stateV.defattr',
    state_V_chain_mapping
)
