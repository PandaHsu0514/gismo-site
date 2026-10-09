# gismo.com.tw 個人網站

網站名稱「勇博講古」。主角是文章（原創＋好文分享，不分主題），其次是教學分享、AI 小作品、AI 遊戲；學術著作放在關於頁，不在主選單。請用繁體中文溝通。

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
