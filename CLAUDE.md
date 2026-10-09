# gismo.com.tw 個人網站

網站名稱「勇博講古」。選單：文章（原創＋好文分享）｜晚安故事（有聲繪本）｜勇博開講（財經，影片放 YouTube 嵌入）｜文獻筆記｜教學｜AI 遊樂場（小作品＋27 款遊戲）｜關於（含學術著作）。請用繁體中文溝通。

設計：宣紙底、墨色字、朱紅印章（`.seal`），標題用 Noto Serif TC。

## 架構
- Eleventy 3，原始檔在 `src/`，輸出到 `_site/`（不進 git）
- 每個項目一個 Markdown 檔：`src/articles/`、`src/teaching/`、`src/works/`、`src/games/`、`src/papers/`（遊戲本體在 `src/play/<名稱>/`）
- 個人資料與導覽列：`src/_data/site.json`；版型：`src/_includes/`；樣式：`src/assets/style.css`（顏色用 `:root` 變數，深色模式要一起改）
- 欄位說明見 `README.md`
- 本機預覽：`npm run dev` → http://localhost:8080

## 部署
- GitHub：`PandaHsu0514/gismo-site`（公開），gh CLI 已登入 PandaHsu0514
- 推到 `main` → GitHub Actions 自動部署到 GitHub Pages，約 1 分鐘後在 https://gismo.com.tw 生效
- 自訂網域已設定；不要再設 `PATH_PREFIX` repo 變數（那只在用 github.io 子路徑時需要）
- commit／push 前先跟使用者確認

## DNS（GoDaddy）
- 網站：`@` A 記錄 ×4 指向 GitHub（185.199.108–111.153），`www` CNAME → pandahsu0514.github.io
- 信箱相關記錄（MX、SPF TXT、SRV autodiscover、CNAME email）不要動
- 使用者目前沒在用 @gismo.com.tw 信箱，正在考慮要不要用
- Claude Code 的自動模式不允許代改 DNS；需要改時請使用者自己在 GoDaddy 操作，再幫忙用 dig 驗證
- 網域自動續約是關閉的，2027-02-23 到期

## SEO／GEO／安全
- 每頁的 title、description、canonical、Open Graph、schema.org JSON-LD 都在 `src/_includes/seo.njk` 自動產生（依網址判斷是文章、論文、遊戲或教案）；新內容只要 front matter 有 title 和 summary／description 就好
- 給 AI 搜尋（GEO）：`/llms.txt`（自動列出全站內容）、`robots.txt` 明確允許 GPTBot、ClaudeBot、PerplexityBot 等
- `/sitemap.xml`、`/feed.xml`（文章 Atom）自動產生；front matter 加 `noindex: true` 可排除
- 安全：`base.njk` 有 CSP meta（GitHub Pages 不能自訂 header）；要嵌入新的外部服務（例如 YouTube 以外的影片）得改 CSP；`/play/` 遊戲頁 noindex；Dependabot 每週檢查套件

## 內容來源與規則
- 晚安故事：來源 `~/Library/Application Support/BedtimeVideo/`，只放完整版、不放樣本；「雲杉林裡小貘的靜靜風箏」「星霧果園裡小鸚鵡的晚安果籃」使用者認為品質不好，不要放；影片一律上傳 YouTube 再填 `youtube` 欄位，不把 MP4 放進網站
- 文獻筆記：來源 `~/Documents/每日文獻閱讀/文獻讀書報告/`，使用者同意全部公開；匯入時去掉內部作業說明，「你」改成第一人稱
- 勇博開講的財經報告（來源 `~/.openclaw/workspace/finance-learning-reports/`）要使用者看過才發布：一律先用 `draft: true` 匯入
- AdSense 尚未申請；兒童內容（晚安故事）不放廣告
- gismo.com.tw 只做個人網站。使用者的 AI token 銷售業務會另外用別的網域經營，不要把販售 token、API 額度的內容放進這個網站
