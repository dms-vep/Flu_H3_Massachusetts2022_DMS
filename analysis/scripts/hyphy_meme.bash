#!/bin/bash
#
#SBATCH -c 32

# conda activate phylo
hyphy meme \
    --alignment ../data/alignments/nodeSeqs_nuc.fasta \
    --tree      ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.nwk \
    --output    ../results/h3n2_ha_60y_meme.json