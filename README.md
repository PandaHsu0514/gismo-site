# gismo.com.tw 個人網站

用 [Eleventy](https://www.11ty.dev/) 產生的靜態網站，推到 GitHub 的 `main` 分支後會自動部署到 GitHub Pages。

## 本機預覽

```sh
npm install      # 第一次才需要
npm run dev      # 打開 http://localhost:8080 ，改檔案會自動重新整理
```

## 新增內容：一個項目就是一個 Markdown 檔

| 要新增 | 放在 | 檔案（PDF、圖片）放在 |
|---|---|---|
| 文章（原創或好文分享） | `src/articles/日期-簡稱.md` | `src/files/articles/` |
| 教案／教學分享 | `src/teaching/日期-簡稱.md` | `src/files/teaching/` |
| 論文 | `src/papers/年份-簡稱.md` | `src/files/papers/` |
| AI 創作 | `src/works/年份-簡稱.md` | `src/files/works/` |
| 小遊戲說明頁 | `src/games/簡稱.md` | 遊戲本體放 `src/play/簡稱/index.html` |

檔名會變成網址，例如 `src/papers/2025-tourism.md` → `gismo.com.tw/papers/2025-tourism/`。
建議用英文小寫和 `-`，不要用空格。最簡單的做法是複製一個範例檔再修改。

### 文章欄位

```yaml
---
title: 文章標題
date: 2026-10-01
summary: 列表上顯示的一兩句摘要
kind: 好文              # 不寫就是「原創」；分享別人的文章寫「好文」
source: 原作者／媒體     # 好文才需要
sourceUrl: https://...   # 好文才需要，頁面上會出現「閱讀原文」
---
內文用 Markdown 寫。
```

### 教學欄位

```yaml
---
title: 教案名稱
date: 2026-09-15
audience: 國中・八年級   # 對象
duration: 2 節課         # 可省略
summary: 一兩句說明
files:                   # 可省略，會變成下載按鈕
  - label: 教案 PDF
    url: /files/teaching/xxx.pdf
---
```

### 論文欄位

```yaml
---
title: 論文標題
authors: 作者一, 作者二
venue: 期刊或研討會名稱
year: 2025
type: 期刊        # 期刊 / 研討會 / 學位論文 / 預印本，列表頁會自動產生篩選按鈕
pdf: /files/papers/2025-tourism.pdf
doi: 10.1016/j.tourman.2017.xx.xxx
abstract: 摘要
---
（可選）延伸說明，可以放圖表或連結。
```

### AI 創作欄位

```yaml
---
title: 作品名稱
description: 一句話介紹（列表卡片會顯示）
kind: 圖像        # 圖像 / 影片 / 音樂 / 文字 / 互動
year: 2025
tools: 使用的工具或模型
cover: /files/works/封面.jpg
link: 外部連結（可選）
---
```

### 小遊戲欄位

```yaml
---
title: 遊戲名稱
description: 一句話介紹
year: 2026
order: 28            # 列表排序，數字小的在前
play: /play/簡稱/
icon: "🎮"           # 卡片上的圖示
category: 動作       # 射擊 / 動作 / 益智 / 棋類 / 休閒，列表頁會自動產生篩選按鈕
gameTags: [動作, 手機可玩]
---
```

遊戲本體是一個獨立的 HTML 檔。共用的配色、分數紀錄、開始／結束畫面、觸控按鈕在 `src/play/kit/`，新遊戲引用 `../kit/kit.css` 和 `../kit/kit.js` 就能跟其他遊戲長得一樣。

## 其他

- 個人資料、導覽列：`src/_data/site.json`
- 關於頁：`src/about.md`（學術著作會自動列在關於頁下方）
- 顏色與版面：`src/assets/style.css`
- 自訂網域：`src/CNAME`（內容是 `gismo.com.tw`）
