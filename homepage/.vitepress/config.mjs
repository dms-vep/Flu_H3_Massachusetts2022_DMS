import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  lang: "en-US",
  title: "Deep mutational scanning of H3 influenza HA",
  description:
    "A collection of data, figures, and analysis for exploring pleiotropic constraints on antigenic evolution.",
  base: "/Flu_H3_Massachusetts2022_DMS/",
  appearance: false,
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Appendix", link: "/appendix", target: "_self" },
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/dms-vep/Flu_H3_Massachusetts2022_DMS" }],
    footer: {
      message: "Built by Timothy Yu and Jesse Bloom",
    },
  },
});
