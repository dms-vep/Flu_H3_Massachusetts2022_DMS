#!/bin/bash
#
#SBATCH -c 32

# 60y build
curl https://nextstrain.org/groups/blab/flu/seasonal/h3n2/ha/60y \
    --header 'Accept: application/vnd.nextstrain.dataset.main+json' \
    --compressed > ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.json

curl https://nextstrain.org/groups/blab/flu/seasonal/h3n2/ha/60y \
    --header 'Accept: application/vnd.nextstrain.dataset.tip-frequencies+json' \
    --compressed > ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_frequencies.json

python3 auspice_tree_to_table.py \
    --include-internal-nodes \
    --tree ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.json \
    --output-metadata ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.tsv \
    --output-tree ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.nwk

python allele_frequencies.py \
    --tree_file ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.nwk \
    --mutations_file ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.tsv \
    --frequencies_file ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_frequencies.json \
    --main_json_file ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.json \
    --fix_cutoff 0.95 \
    --output_frequencies_csv ../results/h3n2_ha_60y_frequencies_df.csv \
    --output_phenotypes_csv ../results/h3n2_ha_60y_phenotypes_df.csv \
    --root_sequence_file ../data/nextstrain_h3n2_ha_60y/root.json

# 12y build
curl https://nextstrain.org/seasonal-flu/h3n2/ha/12y@2025-04-27 \
    --header 'Accept: application/vnd.nextstrain.dataset.main+json' \
    --compressed > ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_nextstrain.json

curl https://nextstrain.org/seasonal-flu/h3n2/ha/12y@2025-04-27 \
    --header 'Accept: application/vnd.nextstrain.dataset.tip-frequencies+json' \
    --compressed > ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_frequencies.json

python3 auspice_tree_to_table.py \
    --include-internal-nodes \
    --tree ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_nextstrain.json \
    --output-metadata ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_nextstrain.tsv \
    --output-tree ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_nextstrain.nwk

python allele_frequencies.py \
    --tree_file ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_nextstrain.nwk \
    --mutations_file ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_nextstrain.tsv \
    --frequencies_file ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_frequencies.json \
    --main_json_file ../data/nextstrain_h3n2_ha_12y/h3n2_ha_12y_nextstrain.json \
    --fix_cutoff 0.95 \
    --output_frequencies_csv ../results/h3n2_ha_12y_frequencies_df.csv \
    --output_phenotypes_csv ../results/h3n2_ha_12y_phenotypes_df.csv