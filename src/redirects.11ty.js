// 舊網址或外部連結用的轉址頁：內容 front matter 寫 aliases: ["/舊網址/"] 就會產生
// /headlines/ 是 OpenClaw 上架包預設的網址，每日頭條實際放在勇博開講（/finance/）
export const data = {
  eleventyExcludeFromCollections: true,
  pagination: {
    data: "collections.all",
    size: 1,
    alias: "r",
    before: (all) => [
      { from: "/headlines/", to: "/finance/" },
      ...all.flatMap((p) => (p.data.aliases || []).map((from) => ({ from, to: p.url }))),
    ],
  },
  permalink: (data) => data.r.from,
};
export const render = ({ r, site }) => `<!doctype html>
<html lang="zh-Hant-TW"><head><meta charset="utf-8">
<title>已搬家</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="${site.url}${r.to}">
<meta http-equiv="refresh" content="0; url=${r.to}">
</head><body><p>此頁已搬到 <a href="${r.to}">${site.url}${r.to}</a></p>
<script>location.replace(${JSON.stringify(r.to)} + location.search + location.hash)</script>
</body></html>
`;
