"""Custom rules used in the ``snakemake`` pipeline.

This file is included by the pipeline ``Snakefile``.

"""

rule nt_changes_to_codon:
    """Annotate how nucleotide changes to codon required for each amino-acid mutation."""
    input:
        natural_geneseq="data/Massachusetts22_H3N2_HA_EPI2413620.fasta",
        site_numbering_map=config["site_numbering_map"],
        pacbio_amplicon=config["pacbio_amplicon"],
    output:
        annotations=config["mutation_annotations"],
    log:
        notebook="results/logs/nt_changes_to_codon.ipynb"
    conda:
        os.path.join(config["pipeline_path"], "environment.yml")
    notebook:
        "analysis/nt_changes_to_codon.ipynb"