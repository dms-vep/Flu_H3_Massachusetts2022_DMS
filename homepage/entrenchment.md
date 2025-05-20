---
aside: false
---

# Analysis of epistatic entrenchment

Evolutionary entrenchment is a form of epistasis in which the contemporary strain has lost tolerance for an ancestral amino acid. 

## Interactive plot
This interactive plot shows the effects of reversions to all ancestral amino acids that were previously fixed in human H3N2 strains since 1968 on HA-mediated cell entry (top row) or HA acid stability (bottom row) as measured in the deep mutational scanning on the MA22 HA. You can mouseover points to view details about the ancestral amino acids (labeled as `mutant`). 

The frequencies of ancestral amino acids were obtained from this [Nextstrain tree](https://nextstrain.org/groups/blab/flu/seasonal/h3n2/ha/60y), and the fixation cutoff was set at 95%. Mutations are placed on the x-axis by the most recent date that the ancestral amino acid was fixed, and the panel columns indicate whether the mutation is at a site inside (left column) or outside (right column) of the receptor binding pocket. The range of the y-axis for each phenotype is set to span the range of effects of all mutations to HA (not just those that fixed during natural H3N2 evolution) in the deep mutational scanning.

Click on the expansion box in the upper right of the plot to enlarge for easier viewing, or click [here](https://dms-vep.org/Flu_H3_Massachusetts2022_DMS/htmls/entrenchment.html) to open the plot in a stand-alone window.

<Figure caption="Epistatic entrenchment of mutation effects on cell entry and acid stability">
    <Altair :showShadow="true" :spec-url="'htmls/entrenchment.html'"></Altair>
</Figure>

## Numerical values
The numerical data plotted on this page can be found [here](https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS/blob/main/analysis/results/h3n2_ha_60y_phenotypes_df.csv).
