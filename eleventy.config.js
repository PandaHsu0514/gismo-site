import { HtmlBasePlugin } from "@11ty/eleventy";

export default function (eleventyConfig) {
  // 網站放在子路徑（例如 github.io/gismo-site/）時，自動替站內連結加上前綴
  eleventyConfig.addPlugin(HtmlBasePlugin);

  // 不經處理、直接複製到網站的檔案
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/files");
  eleventyConfig.addPassthroughCopy("src/play");
  eleventyConfig.addPassthroughCopy("src/CNAME");

  // 文章、教學依日期新到舊；論文、作品、遊戲依年份新到舊，同年份再依檔名
  const byDate = (a, b) => b.date - a.date;
  const byYear = (a, b) => (b.data.year || 0) - (a.data.year || 0) || b.fileSlug.localeCompare(a.fileSlug);
  eleventyConfig.addCollection("articles", (api) => api.getFilteredByGlob("src/articles/*.md").sort(byDate));
  eleventyConfig.addCollection("teaching", (api) => api.getFilteredByGlob("src/teaching/*.md").sort(byDate));
  eleventyConfig.addCollection("papers", (api) => api.getFilteredByGlob("src/papers/*.md").sort(byYear));
  eleventyConfig.addCollection("works", (api) => api.getFilteredByGlob("src/works/*.md").sort(byYear));
  eleventyConfig.addCollection("games", (api) => api.getFilteredByGlob("src/games/*.md").sort(byYear));

  eleventyConfig.addFilter("uniq", (items, key) => [...new Set(items.map((i) => i.data[key]).filter(Boolean))]);
  eleventyConfig.addFilter("first", (items, n) => items.slice(0, n));
  // 2026-10-01 → 2026.10.01
  eleventyConfig.addFilter("ymd", (d) => new Date(d).toISOString().slice(0, 10).replaceAll("-", "."));
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString().slice(0, 10));

  return {
    dir: { input: "src", output: "_site" },
    markdownTemplateEngine: false,
    htmlTemplateEngine: "njk",
    pathPrefix: process.env.PATH_PREFIX || "/",
  };
}
