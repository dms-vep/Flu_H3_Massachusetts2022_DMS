---
aside: false
---

# Summary on effects of mutations on all measured phenotypes

## Interactive plot
The plots below show how mutations affect neutralization by human sera, cell entry, and acid stability. These plots are interactive, and allow you to zoom and mouseover sites and mutations.
- The **zoom bar** at the top of the plot shows different regions of HA, and can be used to zoom in on specific sites.
- The faceted **line plot** summarizes the effects of mutations on sera neutralization at each site (more positive values indicate more escape, more negative values indicate more sensitizing). The escape at a site is quantified using the site summary statistic specified by the interactive option at the bottom of the plot (e.g., sum or mean effect of mutations at a site).
- The **heatmaps** show how each individual mutation affects sera neutralization, cell entry, and acid stability. The sera neutralization values are averaged across all sera mapped. The `X`'s indicate the amino-acid identity in the A/Massachusetts/18/2022(H3N2) strain. Note the two different shades of gray have different meanings: dark gray tiles indicate mutations that are too deleterious for cell entry to reliably measure their effect on acid stability or sera neutralization, while light gray tiles indicate mutations that were missing (not measured) in the library.

Click on the expansion box in the upper right of the plot to enlarge for easier viewing, or click [here](https://dms-vep.org/Flu_H3_Massachusetts2022_DMS/htmls/Phenotypes_faceted.html) to open the plot in a stand-alone window.

<Figure caption="">
    <Altair :showShadow="true" :spec-url="'htmls/Phenotypes_faceted.html'"></Altair>
</Figure>

## Numerical values
The **pre-filtered** cell entry and acid stability data plotted on this page can be found [here](https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS/blob/main/results/summaries/Phenotypes.csv). The **pre-filtered** sera neutralization data plotted on this page can be found [here](https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS/blob/main/results/summaries/Phenotypes_per_antibody_escape.csv).