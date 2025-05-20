---
aside: false
---

# Effects of mutations on HA acid stability

## Interactive plot
The plots below show how mutations affect acid stability. These plots are interactive, and allow you to zoom and mouseover sites and mutations.
- The **zoom bar** at the top of the plot shows different regions of HA, and can be used to zoom in on specific sites.
- The **line plot** summarizes the effects of mutations on acid stability at each site (more negative values indicate decreased acid stability). The acid stability at a site is quantified using the site summary statistic specified by the interactive option at the bottom of the plot (e.g., mean effect of mutations at a site).
- The **heatmap** shows how each individual mutation affects acid stability. The `X`'s indicate the amino-acid identity in the A/Massachusetts/18/2022(H3N2) strain. Note the two different shades of gray have different meanings: dark gray tiles indicate mutations that are too deleterious for cell entry to reliably measure their effect on acid stability, while light gray tiles indicate mutations that were missing (not measured) in the library.

Click on the expansion box in the upper right of the plot to enlarge for easier viewing, or click [here](https://dms-vep.org/Flu_H3_Massachusetts2022_DMS/htmls/stability_mut_effect.html) to open the plot in a stand-alone window.

<Figure caption="">
    <Altair :showShadow="true" :spec-url="'htmls/stability_mut_effect.html'"></Altair>
</Figure>

For a wrapped version of the heatmap, click [here](https://dms-vep.org/Flu_H3_Massachusetts2022_DMS/htmls/stability_wrapped_heatmap.html).

## Numerical values
The **pre-filtered** numerical data plotted on this page can be found [here](https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS/blob/main/results/summaries/Phenotypes.csv). Alternatively, the **unfiltered** data are available [here](https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS/blob/main/results/stability/averages/stability_mut_effect.csv). Note the unfiltered data have not been filtered for QC criteria like `times_seen`, so either make sure you understand the filters in the file or we recommend just using the pre-filtered data.