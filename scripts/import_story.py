#!/usr/bin/env python3
"""把 OpenClaw 做好的有聲繪本資料夾，轉成網站的「晚安故事」。

用法：python3 scripts/import_story.py <繪本資料夾> <網址代稱 slug> [--date YYYY-MM-DD]
- 繪本資料夾要已經跑過 finish_picturebook.sh（有 narration-pages.txt、images/illustration-NN.png、audio/page-NN.m4a）
- 有 storyboard.json 時，同一場景的幾頁共用一張圖（只輸出場景數量的 JPG）
- 圖片用 macOS 的 sips 縮成 540×960 JPEG；音檔直接複製 m4a；不放 MP4（影片另外上傳 YouTube 再填 youtube 欄位）
- 已存在同名 slug 就停止，不覆寫
- 匯入後自動重跑 build_story_font.py，讓新故事的字也有注音
"""
import hashlib, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
argv = sys.argv[1:]
if "--date" in argv:
    k = argv.index("--date"); argv = argv[:k] + argv[k + 2:]
args = [a for a in argv if not a.startswith("--")]
if len(args) != 2:
    sys.exit(__doc__)
book, slug = os.path.abspath(args[0]), args[1]
date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else os.path.basename(book)[:10]
md = f"{ROOT}/src/stories/{slug}.md"
out = f"{ROOT}/src/files/stories/{slug}"
if os.path.exists(md) or os.path.exists(out):
    sys.exit(f"已經有 {slug}，不覆寫")

title = re.sub(r"^\d{4}-\d\d-\d\d-", "", os.path.basename(book))
texts = [x.strip() for x in open(f"{book}/narration-pages.txt", encoding="utf-8").read().split("\n\n") if x.strip()]
n = len(texts)
for i in range(1, n + 1):
    for f in (f"{book}/images/illustration-{i:02}.png", f"{book}/audio/page-{i:02}.m4a"):
        if not os.path.isfile(f):
            sys.exit(f"缺 {f}（先跑 finish_picturebook.sh）")

# 每頁用哪張圖：內容相同的插圖只輸出一次
os.makedirs(out)
img_of, made = {}, {}
for i in range(1, n + 1):
    src = f"{book}/images/illustration-{i:02}.png"
    h = hashlib.md5(open(src, "rb").read()).hexdigest()
    if h not in made:
        name = f"p{len(made) + 1:02}.jpg"
        subprocess.run(["sips", "-z", "960", "540", "-s", "format", "jpeg", "-s", "formatOptions", "72", src, "--out", f"{out}/{name}"],
                       check=True, capture_output=True)
        made[h] = name
    img_of[i] = made[h]
    shutil.copy(f"{book}/audio/page-{i:02}.m4a", f"{out}/a{i:02}.m4a")

summary = ""
for t in texts:
    summary += t
    if len(summary) >= 70:
        break
fm = {"title": title, "date": date, "summary": summary if len(summary) <= 100 else summary[:98] + "…",
      "cover": f"/files/stories/{slug}/{img_of[1]}",
      "pages": [{"img": f"/files/stories/{slug}/{img_of[i]}", "text": texts[i - 1], "audio": f"/files/stories/{slug}/a{i:02}.m4a"} for i in range(1, n + 1)],
      "youtube": ""}
with open(md, "w", encoding="utf-8") as fh:
    fh.write("---json\n" + json.dumps(fm, ensure_ascii=False, indent=1) + "\n---\n")
# 注音字型只含已上架故事的用字，新故事有新字就要重新產生
subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_story_font.py")], check=True)
print(json.dumps({"slug": slug, "title": title, "pages": n, "images": len(made)}, ensure_ascii=False))
