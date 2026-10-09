// AdSense 的 ads.txt：site.json 填了 adsense.client 才會產生
export const data = {
  eleventyExcludeFromCollections: true,
  permalink: (data) => (data.site.adsense.client ? "/ads.txt" : false),
};
export const render = (data) => `google.com, ${data.site.adsense.client.replace(/^ca-/, "")}, DIRECT, f08c47fec0942fa0\n`;
