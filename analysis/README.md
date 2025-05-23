# Analysis

This directory contains custom analyses that reproduce figures in the paper. These analyses are not run as part of the Snakemake pipeline.

## Entrenchment analysis
To calculate historical allele frequencies, first enter the Nextstrain shell.
```
cd scripts
nextstrain shell .
```

Then run the following to get the frequencies.
```
sbatch -c 8 allele_frequencies.bash
```

The notebook [entrenchment.ipynb](entrenchment.ipynb) produces the plots in Figure 3.