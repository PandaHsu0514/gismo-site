# gismo.com.tw 個人網站

網站名稱「勇博講古」。選單：勇博開講（財經，影片放 YouTube 嵌入）｜文獻筆記｜教學｜AI 小工具（`src/tools/`，純瀏覽器端工具）｜AI 遊樂場（小作品＋28 款遊戲）｜晚安故事（有聲繪本）｜關於（含學術著作，固定最後）。「文章」（原創＋好文分享，`/articles/`）頁面還在，但使用者要求不放在選單。請用繁體中文溝通。

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
- commit／push 前先跟使用者確認。例外：文獻筆記由每日排程自動匯入並推送（使用者已同意全自動上架）

## DNS（GoDaddy）
- 網站：`@` A 記錄 ×4 指向 GitHub（185.199.108–111.153），`www` CNAME → pandahsu0514.github.io
- 郵件（2026-10-09 確認）：GoDaddy 沒有任何郵件服務；使用者已自行刪除 MX，所以 @gismo.com.tw 目前收不到信。2026-10-09 已改成防冒用設定：SPF `v=spf1 -all`、DMARC `v=DMARC1; p=reject`（宣告此網域不寄信）。SRV autodiscover 與 CNAME email 還在。之後要啟用信箱時，這兩筆要改回對應服務的設定
- 使用者決定郵件先不處理。之後若要用，建議做法：把 gismo.com.tw 加進 esad.cc 的 Google Workspace 當「使用者別名網域」（esad.cc 用 Google Workspace），MX 設 `smtp.google.com`、SPF 改 `v=spf1 include:_spf.google.com ~all`、加 DKIM；esad.cc 本身也缺 SPF 記錄
- Claude Code 的自動模式不允許代改 DNS；需要改時請使用者自己在 GoDaddy 操作，再幫忙用 dig 驗證
- 網域自動續約是關閉的，2027-02-23 到期

## SEO／GEO／安全
- 每頁的 title、description、canonical、Open Graph、schema.org JSON-LD 都在 `src/_includes/seo.njk` 自動產生（依網址判斷是文章、論文、遊戲或教案）；新內容只要 front matter 有 title 和 summary／description 就好
- 給 AI 搜尋（GEO）：`/llms.txt`（自動列出全站內容）、`robots.txt` 明確允許 GPTBot、ClaudeBot、PerplexityBot 等
- `/sitemap.xml`、`/feed.xml`（文章 Atom）自動產生；front matter 加 `noindex: true` 可排除
- 統計：Google Analytics 4（Firebase 專案 dryungtalk，掛在 esad.cc 組織下，Spark 免費方案、不綁付款方式；評估 ID 在 `site.json` 的 `ga` 和 `src/play/kit/ga.js`）。網站頁面由 `base.njk` 載入、遊戲頁各自載入 `../kit/ga.js`；只在 gismo.com.tw 上送資料；晚安故事（`noAnalytics: true`）不載入。修仙遊戲送 xx_birth／xx_path／xx_quest／xx_break／xx_death 事件
- 安全：`base.njk` 有 CSP meta（GitHub Pages 不能自訂 header）；要嵌入新的外部服務（例如 YouTube 以外的影片）得改 CSP；`/play/` 遊戲頁 noindex；Dependabot 每週檢查套件

## 內容來源與規則
- 晚安故事：來源 OpenClaw 的 `bedtime-story/picturebooks/`（外接碟），用繪本審核台核准上架（見下方）；只放完整版、不放樣本；「雲杉林裡小貘的靜靜風箏」「星霧果園裡小鸚鵡的晚安果籃」使用者認為品質不好，不要放；影片一律上傳 YouTube 再填 `youtube` 欄位，不把 MP4 放進網站
- 文獻筆記：來源 `~/Documents/每日文獻閱讀/文獻讀書報告/`，以及 Google Drive（panda@esad.cc）`我的雲端硬碟/workspace/journal-reading-reports`、`journal-reading-reports 1`（本機路徑 `~/Library/CloudStorage/GoogleDrive-panda@esad.cc/`）。使用者同意全部公開；同一篇論文只留最完整的一份；不放使用者自己論文的筆記；匯入時去掉內部作業說明（選題理由、PDF 路徑等），「你」改成第一人稱；每篇要有中文標題（`title`），英文原題放 `paperTitle`；`category` 用 教育／管理／行銷／觀光／AI 應用／研究方法／理論
- 財經內容（OpenClaw 的 `finance-learning-reports/`）2026-10-22 使用者決定**不放上 gismo.com.tw**，不要匯入；`src/finance/` 現有 6 篇草稿維持 `draft: true` 不發布
- AdSense 尚未申請；兒童內容（晚安故事）不放廣告
- gismo.com.tw 只做個人網站。使用者的 AI token 銷售業務會另外用別的網域經營，不要把販售 token、API 額度的內容放進這個網站

## 文獻筆記自動上架
- `scripts/publish-notes.sh` 每天 13:00 由 launchd 執行（`~/Library/LaunchAgents/tw.gismo.publish-notes.plist`），紀錄在 `~/Library/Logs/gismo-publish-notes.log`，完成或失敗會跳 Mac 通知
- 來源：2026-10-11 起 OpenClaw workspace 在外接碟 `/Volumes/mac Ds - Data/Offload/openclaw/workspace/`（Drive 只剩舊報告，且只在雲端的檔案背景讀會出 Errno 11 或卡住，所以不再讀 Drive）；外接碟沒接上就會失敗
- 流程：git pull → `scripts/import_notes.py` 匯入新報告 → 先建置網站確認沒壞 → 只 commit `src/notes`、`src/files/notes`、Crossref 快取 → push
- 匯入規則寫在 `import_notes.py` 開頭；中文標題與分類讀 OpenClaw 報告裡的「## 網站上架資訊」（規格寫在外接碟 workspace 的 `journal-agent-pipeline-prompt.md` Step 6；2026-10-22 補回，搬家時漏掉了）
- 匯入只新增不覆寫，手動修改過的筆記（標題、分類）不會被蓋掉
- 要下架某篇：刪掉 `src/notes/` 的檔案和 `src/files/notes/` 的圖，並把它的 DOI（沒有 DOI 就用英文標題）加進 `scripts/data/notes-removed.json`，否則隔天會被重新匯入
- 停用：`launchctl bootout gui/$(id -u)/tw.gismo.publish-notes`

## 繪本審核台（本機）
- `npm run review` 開 http://127.0.0.1:8090（只聽本機、網址帶隨機 token；`review/` 不在 `src/`，不會進網站）
- 列出 OpenClaw `picturebooks/` 裡收尾完成、還沒上架的書，自動檢查頁數、分鏡對應、SVG 假圖、鏡頭種類；核准 → `import_story.py` 匯入＋建置檢查 → 按「推上網站」才 commit／push（等於使用者確認）；可撤銷核准、退回（原因寫進繪本資料夾 `REVIEW-REJECTED.md` 給 OpenClaw）
- 上架／退回紀錄在 `scripts/data/stories-review.json`；網站已有同名故事的也算已上架
