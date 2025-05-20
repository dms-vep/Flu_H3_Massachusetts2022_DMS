---
layout: home

hero:
  name: "Deep mutational scanning of H3 influenza HA"
  tagline: "A collection of data, figures, and analysis for exploring pleiotropic constraints on the antigenic evolution of human H3N2 influenza virus."
  image: MA22_MDCKSIAT1_entry_mean.png
features:
  - title: Cell entry
    details: Effects of mutations on cell entry
    link: /cell_entry
  - title: Acid stability
    details: Effects of mutations on acid stability
    link: /acid_stability
  - title: Sera neutralization
    details: Effects of mutations on neutralization by human sera
    link: /sera_neutralization
  - title: Epistatic entrenchment
    details: Explore if mutation effects have become entrenched
    link: /entrenchment
  - title: Summary
    details: Explore how mutations affect all measured phenotypes together
    link: /summary
---

## Overview
This site hosts interactive visualizations from deep mutational scanning experiments that measure the effects of mutations to the HA of A/Massachusetts/18/2022 (H3N2) influenza virus. Clicking on the links in the boxes above will take you to pages that access the visualizations.

This work was performed in the [Bloom lab](https://jbloomlab.org/). To read the paper that describes the results, see [Yu et al (2025)]().

Note that the experiments were performed using [pseudovirus deep mutational scanning](https://doi.org/10.1016/j.cell.2023.02.001). These pseudoviruses encode no viral genes other than HA, and so can only undergo a **single** round of cell entry. These pseudoviruses are therefore not infectious agents and are not disease-causing pathogens, and so provide a safe way to study HA mutations at biosafety-level 2.

All of the plots and files here use the widely adopted **H3 numbering scheme**. This numbering starts with one at the first amino-acid of the ectodomain, not the N-terminal methionine. Click [here](https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS/blob/main/data/site_numbering_map.csv) for the site numbering map.

The GitHub repository with the full analysis and code is at [https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS](https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS/) and the full output of the analysis pipeline is in the [Appendix](appendix.html){target="_self"}.