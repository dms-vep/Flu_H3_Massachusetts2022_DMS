# Download root sequence sidecar JSON.
curl https://nextstrain.org/groups/blab/flu/seasonal/h3n2/ha/60y \
    --header 'Accept: application/vnd.nextstrain.dataset.root-sequence+json' \
    --compressed > ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_root-sequence.json

# Extract multiple sequence alignment for HA1 gene.
python node_seqs_for_gene.py \
    --gene HA1 \
    --local-files \
    --tree ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.json \
    --root ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_root-sequence.json \
    --outdir ../data/alignments

# Extract multiple sequence alignment for HA2 gene.
python node_seqs_for_gene.py \
    --gene HA2 \
    --local-files \
    --tree ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.json \
    --root ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_root-sequence.json \
    --outdir ../data/alignments

# Extract multiple sequence alignment for nuc.
python node_seqs_for_gene.py \
    --gene nuc \
    --local-files \
    --tree ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_nextstrain.json \
    --root ../data/nextstrain_h3n2_ha_60y/h3n2_ha_60y_root-sequence.json \
    --outdir ../data/alignments