#!/usr/bin/env python3
"""
Adapted from Kistler et al. 2023 https://bedford.io/papers/kistler-atlas-viral-evolution/

Given a tree.json and root-sequence.json file, finds the sequences of
each node in the tree and outputs a FASTA file with these node sequences.
If a gene is specified, the sequences will be the AA sequence of that gene
at that node. If 'nuc' is specified, the whole genome nucleotide sequence
at the node will be output. (this is default if no gene is specified).
The FASTA header is the node's name in the tree.json
"""
import argparse
import json
import requests
from augur.utils import json_to_tree
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import MutableSeq
from Bio.SeqRecord import SeqRecord


def apply_muts_to_root(root_seq, list_of_muts):
    """
    Apply a list of mutations to the root sequence
    to find the sequence at a given node. The list of mutations
    is ordered from root to node, so multiple mutations at the
    same site will correctly overwrite each other
    """

    # make the root sequence mutatable
    root_plus_muts = MutableSeq(root_seq)

    # apply all mutations to root sequence
    for mut in list_of_muts:
        # subtract 1 to deal with biological numbering vs python
        mut_site = int(mut[1:-1])-1
        # get the nuc that the site was mutated TO
        mutation = mut[-1]
        # apply mutation
        root_plus_muts[mut_site] = mutation


    return root_plus_muts


def getNodeSequences(gene, local_files, tree_file, root_file, outdir):
    """
    Get the sequence at each node in the given tree and
    save them as a FASTA file
    """
    # if we are fetching the JSONs from a URL
    if not local_files:
        # fetch the tree JSON from URL
        tree_json = requests.get(tree_file, headers={"accept":"application/json"}).json()
        # put tree in Bio.phylo format
        tree = json_to_tree(tree_json)
        # fetch the root JSON from URL
        root_json = requests.get(root_file, headers={"accept":"application/json"}).json()
        # get the nucleotide sequence of root
        root_seq_nuc = root_json[gene]

    # if we are using paths to local JSONs
    elif local_files:
        # load tree
        with open(tree_file, 'r') as f:
            tree_json = json.load(f)
        # put tree in Bio.phylo format
        tree = json_to_tree(tree_json)
        # load root sequence file
        with open(root_file, 'r') as f:
            root_json = json.load(f)
        # get the nucleotide sequence of root
        root_seq_nuc = root_json[gene]

    ## Now find the node sequences

    # initialize list to store sequence records for each node
    sequence_records = []

    # find sequence at each node in the tree (includes internal nodes and terminal nodes)
    for node in tree.find_clades(terminal=True):

        # get path back to the root
        path = tree.get_path(node)

        # get all nucleotide mutations relative to root
        nt_muts = [branch.branch_attrs['mutations'].get(gene, []) for branch in path]
        # flatten the list of nucleotide mutations
        nt_muts = [item for sublist in nt_muts for item in sublist]
        # get sequence at node
        node_seq = apply_muts_to_root(root_seq_nuc, nt_muts)
        # remove stop codon if gene is nuc
        if gene == 'nuc':
            if len(node_seq) % 3 == 0:
                node_seq = node_seq[:-3]
            else:
                return ValueError(f"Node {node.name} length not divisible by 3.")

        sequence_records.append(SeqRecord(node_seq, node.name, '', ''))
    
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / f"nodeSeqs_{gene}.fasta"

    SeqIO.write(sequence_records, outfile, "fasta")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--gene", default="nuc",
        help="Name of gene to return AA sequences for. 'nuc' will return full geneome nucleotide seq")
    parser.add_argument("--local-files", action="store_true",
        help="Toggle this on if you are supplying local JSON files for the tree and root sequence." +
             "Default is to fetch them from a URL")
    parser.add_argument("--tree", default="https://data.nextstrain.org/ncov_gisaid_global_all-time.json",
        help="URL for the tree.json file, or path to the local JSON file if --local-files=True")
    parser.add_argument("--root", default="https://data.nextstrain.org/ncov_gisaid_global_all-time_root-sequence.json",
        help="URL for the root-sequence.json file, or path to the local JSON file if --local-files=True")
    parser.add_argument("--outdir", default=".",
        help="Directory where the output FASTA will be written")

    args = parser.parse_args()

    getNodeSequences(args.gene, args.local_files, args.tree, args.root, args.outdir)