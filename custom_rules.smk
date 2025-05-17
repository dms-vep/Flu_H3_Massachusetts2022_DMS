"""Custom rules used in the ``snakemake`` pipeline.

This file is included by the pipeline ``Snakefile``.

"""

# Annotate nucleotide changes to codon for mutations -------------------------------------
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

# Make row-wrapped heatmaps -------------------------------------------------------------

# read configuration for wrapped heatmaps
with open("data/wrapped_heatmap_config.yaml") as f:
    wrapped_heatmap_config = yaml.YAML(typ="safe", pure=True).load(f)

rule wrapped_heatmap:
    """Make row-wrapped heatmaps."""
    input:
        data_csv=lambda wc: wrapped_heatmap_config[wc.wrapped_hm]["data_csv"],
    output:
        chart_html="results/wrapped_heatmaps/{wrapped_hm}_wrapped_heatmap.html",
        nb="results/notebooks/wrapped_heatmap_{wrapped_hm}.ipynb",
    params:
        params_dict=lambda wc: wrapped_heatmap_config[wc.wrapped_hm]
    log:
        notebook="results/notebooks/wrapped_heatmap_{wrapped_hm}.ipynb",
    conda:
        os.path.join(config["pipeline_path"], "environment.yml"),
    notebook:
        "analysis/wrapped_heatmap.ipynb"

docs["Heatmaps"] = {
    "Heatmap HTMLs" : {
        wrapped_hm: rules.wrapped_heatmap.output.chart_html.format(wrapped_hm=wrapped_hm)
        for wrapped_hm in wrapped_heatmap_config
    }
}

# Entrenchment analysis -------------------------------------------------------------
rule entrenchment_analysis:
    """Perform entrenchment analysis using 60y subsampled tree."""
    input:
        phenotypes_and_freqs="analysis/results/h3n2_ha_60y_phenotypes_df.csv",
        site_numbering_map=config["site_numbering_map"],
    output: 
        chart_html="results/entrenchment/entrenchment.html",
        nb="results/notebooks/entrenchment.ipynb"
    log:
        notebook="results/notebooks/entrenchment.ipynb",
    conda:
        os.path.join(config["pipeline_path"], "environment.yml"),
    notebook:
        "analysis/entrenchment.ipynb"

docs["Entrenchment"] = {
    "Notebook for analyzing entrenchment" : rules.entrenchment_analysis.output.nb,
    "Plot visualizing entrenchment of mutation effects" : rules.entrenchment_analysis.output.chart_html,
}