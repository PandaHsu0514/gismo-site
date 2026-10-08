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
| 論文 | `src/papers/年份-簡稱.md` | `src/files/papers/` |
| AI 創作 | `src/works/年份-簡稱.md` | `src/files/works/` |
| 小遊戲說明頁 | `src/games/簡稱.md` | 遊戲本體放 `src/play/簡稱/index.html` |

檔名會變成網址，例如 `src/papers/2025-tourism.md` → `gismo.com.tw/papers/2025-tourism/`。
建議用英文小寫和 `-`，不要用空格。最簡單的做法是複製一個範例檔再修改。

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
year: 2025
play: /play/簡稱/
gameTags: [標籤一, 標籤二]
---
```

## 其他

- 個人資料、導覽列：`src/_data/site.json`
- 關於頁：`src/about.md`
- 顏色與版面：`src/assets/style.css`
- 自訂網域：`src/CNAME`（內容是 `gismo.com.tw`）
