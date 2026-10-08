import { HtmlBasePlugin } from "@11ty/eleventy";

export default function (eleventyConfig) {
  // 網站放在子路徑（例如 github.io/gismo-site/）時，自動替站內連結加上前綴
  eleventyConfig.addPlugin(HtmlBasePlugin);

  // 不經處理、直接複製到網站的檔案
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/files");
  eleventyConfig.addPassthroughCopy("src/play");
  eleventyConfig.addPassthroughCopy("src/CNAME");

  // 依年份新到舊排序；同年份再依檔名
  const byYear = (a, b) => (b.data.year || 0) - (a.data.year || 0) || b.fileSlug.localeCompare(a.fileSlug);
  eleventyConfig.addCollection("papers", (api) => api.getFilteredByGlob("src/papers/*.md").sort(byYear));
  eleventyConfig.addCollection("works", (api) => api.getFilteredByGlob("src/works/*.md").sort(byYear));
  eleventyConfig.addCollection("games", (api) => api.getFilteredByGlob("src/games/*.md").sort(byYear));

  eleventyConfig.addFilter("uniq", (items, key) => [...new Set(items.map((i) => i.data[key]).filter(Boolean))]);
  eleventyConfig.addFilter("first", (items, n) => items.slice(0, n));

  return {
    dir: { input: "src", output: "_site" },
    markdownTemplateEngine: false,
    htmlTemplateEngine: "njk",
    pathPrefix: process.env.PATH_PREFIX || "/",
  };
}
