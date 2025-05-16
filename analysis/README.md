# Analysis

This directory contains custom analyses that reproduce figures in the paper. These analyses are not run as part of the Snakemake pipeline.

## Cell entry figures
The notebook [analyze_cell_entry.ipynb](analyze_cell_entry.ipynb) produces the plots in Figure 1.

## Stability figures
The notebook [analyze_stability.ipynb](analyze_stability.ipynb) produces the plots in Figure 2.

## Entrenchment figures
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

##  Structures


