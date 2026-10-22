#!/usr/bin/env python3
"""產生晚安故事用的注音網頁字型 src/assets/fonts/story-bpmf.woff2。

從「字嗨注音標楷」（But Ko，https://github.com/ButTaiwan/bpmfvs）只抽出 src/stories/ 裡用到的字，
另外保留注音符號、聲調與破音字選擇符（IVS），所以檔案只有幾百 KB（原檔 17 MB）。
授權：漢字 CC-BY 4.0、其餘 SIL OFL 1.1；OFL 規定修改版不能用保留名稱「字嗨／Zihi」，所以網頁上叫 StoryBpmf。
新增或修改故事後要重跑（import_story.py 會自動呼叫）。

用法：python3 scripts/build_story_font.py
需要 uv（用 uv run 臨時帶 fonttools、brotli，不必另外安裝）。
"""
import glob, json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.environ.get("BPMF_FONT") or "/Volumes/mac Ds - Data/Offload/openclaw/workspace/bedtime-story/assets/fonts/BpmfZihiKaiStd/BpmfZihiKaiStd-Regular.ttf"
OUT = os.path.join(ROOT, "src", "assets", "fonts", "story-bpmf.woff2")
# 注音符號、擴充注音、聲調符號、異體字選擇符（破音字用）
UNICODES = "U+3100-312F,U+31A0-31BF,U+02C7,U+02CA,U+02CB,U+02D9,U+FE00-FE0F,U+E01E0-E01EF"

if not os.path.isfile(SOURCE):
    sys.exit(f"找不到原始字型 {SOURCE}（外接碟沒接上？可用環境變數 BPMF_FONT 指定）")

chars = set()
for f in glob.glob(os.path.join(ROOT, "src", "stories", "*.md")):
    t = open(f, encoding="utf-8").read()
    fm = json.loads(t.split("---json\n", 1)[1].split("\n---", 1)[0])
    chars |= set(fm["title"])
    for p in fm.get("pages", []):
        chars |= set(p["text"])

with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as tf:
    tf.write("".join(sorted(chars)))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
subprocess.run(["uv", "run", "-q", "--no-project", "--with", "fonttools", "--with", "brotli",
                "pyftsubset", SOURCE, f"--text-file={tf.name}", f"--unicodes={UNICODES}",
                "--layout-features=*", "--flavor=woff2", f"--output-file={OUT}"], check=True)
os.remove(tf.name)
print(json.dumps({"chars": len(chars), "bytes": os.path.getsize(OUT)}))
