import { HtmlBasePlugin } from "@11ty/eleventy";

export default function (eleventyConfig) {
  // 網站放在子路徑（例如 github.io/gismo-site/）時，自動替站內連結加上前綴
  eleventyConfig.addPlugin(HtmlBasePlugin);

  // 不經處理、直接複製到網站的檔案
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/files");
  eleventyConfig.addPassthroughCopy("src/play");
  eleventyConfig.addPassthroughCopy("src/CNAME");
  eleventyConfig.addPassthroughCopy({ "src/well-known": ".well-known" });

  // 文章、教學依日期新到舊；論文、作品依年份新到舊，同年份再依檔名；遊戲依 order 欄位
  const byDate = (a, b) => b.date - a.date;
  // 草稿只在本機預覽（npm run dev）出現
  const showDraft = (p) => !p.data.draft || process.env.ELEVENTY_RUN_MODE !== "build";
  const byYear = (a, b) => (b.data.year || 0) - (a.data.year || 0) || b.fileSlug.localeCompare(a.fileSlug);
  eleventyConfig.addCollection("articles", (api) => api.getFilteredByGlob("src/articles/*.md").sort(byDate));
  eleventyConfig.addCollection("stories", (api) => api.getFilteredByGlob("src/stories/*.md").sort(byDate));
  eleventyConfig.addCollection("notes", (api) => api.getFilteredByGlob("src/notes/*.md").sort(byDate));
  eleventyConfig.addCollection("finance", (api) => api.getFilteredByGlob("src/finance/*.md").filter(showDraft).sort(byDate));
  // 首頁「最近講的」：文章、勇博開講、文獻筆記混在一起依日期排（晚安故事有自己的書架）
  eleventyConfig.addCollection("recent", (api) =>
    api.getFilteredByGlob(["src/articles/*.md", "src/finance/*.md", "src/notes/*.md"]).filter((p) => !p.data.draft).sort(byDate));
  eleventyConfig.addCollection("teaching", (api) => api.getFilteredByGlob("src/teaching/*.md").sort(byDate));
  eleventyConfig.addCollection("papers", (api) => api.getFilteredByGlob("src/papers/*.md").sort(byYear));
  eleventyConfig.addCollection("works", (api) => api.getFilteredByGlob("src/works/*.md").sort(byYear));
  eleventyConfig.addCollection("games", (api) => api.getFilteredByGlob("src/games/*.md").sort((a, b) => (a.data.order || 999) - (b.data.order || 999)));

  eleventyConfig.addFilter("uniq", (items, key) => [...new Set(items.map((i) => i.data[key]).filter(Boolean))]);
  eleventyConfig.addFilter("first", (items, n) => items.slice(0, n));
  eleventyConfig.addFilter("navActive", (item, url) => [item.url, ...(item.also || [])].some((u) => url.startsWith(u)));
  // 文獻筆記各分類的篇數，依篇數多到少
  eleventyConfig.addFilter("catCounts", (items) => {
    const c = {};
    items.forEach((i) => i.data.category && (c[i.data.category] = (c[i.data.category] || 0) + 1));
    return Object.entries(c).sort((a, b) => b[1] - a[1]);
  });
  eleventyConfig.addFilter("pluck", (items, key) => items.map((i) => i[key]));
  // 所有文章類集合的主題標籤，依出現次數排序
  eleventyConfig.addFilter("tagCounts", (items, key) => {
    const c = {};
    items.forEach((i) => (i.data[key] || []).forEach((t) => (c[t] = (c[t] || 0) + 1)));
    return Object.entries(c).sort((a, b) => b[1] - a[1]).map(([t]) => t);
  });

  // 草稿（draft: true）只在本機預覽時看得到，不會發布到網站
  eleventyConfig.addPreprocessor("drafts", "*", (data) => {
    if (data.draft && process.env.ELEVENTY_RUN_MODE === "build") return false;
  });
  // 2026-10-01 → 2026.10.01
  eleventyConfig.addFilter("ymd", (d) => new Date(d).toISOString().slice(0, 10).replaceAll("-", "."));
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString().slice(0, 10));
  eleventyConfig.addFilter("isoDateTime", (d) => new Date(d).toISOString());

  // SEO／結構化資料用
  // 轉成 JSON-LD；把 < 換掉，避免內容裡的字串提早結束 <script>
  eleventyConfig.addFilter("jsonld", (obj) => JSON.stringify(obj).replace(/</g, "\\u003c"));
  eleventyConfig.addFilter("authorList", (s) => (s || "").split(/,\s*/).filter(Boolean).map((name) => ({ "@type": "Person", name })));
  eleventyConfig.addFilter("journalName", (s) => (s || "").split(",")[0].trim());
  eleventyConfig.addFilter("xmlEscape", (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"));

  return {
    dir: { input: "src", output: "_site" },
    markdownTemplateEngine: false,
    htmlTemplateEngine: "njk",
    pathPrefix: process.env.PATH_PREFIX || "/",
  };
}
