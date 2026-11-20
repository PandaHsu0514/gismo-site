#!/usr/bin/env python3
"""把 Spark／OpenClaw 的每日晨報匯入網站「每日晨報」（/briefings/），公開精簡版（2026-11-20 使用者決定）。

用法：python3 scripts/import_briefings.py [--dry-run]；最後一行輸出 {"new": [{date, title}], "skipped": [{date, reason}]}
- 來源：Google Drive workspace/daily-briefings/YYYY-MM-DD-morning-news.md，讀不到就用外接碟 OpenClaw workspace 的同名資料夾
- 只放「今日 5 則重要新聞」：標題、摘要、影響；台股補充（法人、個股排行、技術分析、實務觀察與建議）、資料限制一律不放
- 「影響」裡含操作建議字眼（追價、布局、買賣、停損…）的句子拿掉，避免被當成投資建議
- 只匯入 START 之後的晨報；只新增不覆寫，手動改過的不會被蓋掉；解析不到 3 則新聞就跳過並回報（格式可能改了）
- 要下架某天：刪掉 src/briefings/ 的檔案，並把日期加進 scripts/data/briefings-removed.json，否則會被重新匯入
"""
import datetime, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = [os.path.expanduser("~/Library/CloudStorage/GoogleDrive-panda@esad.cc/我的雲端硬碟/workspace/daily-briefings"),
           "/Volumes/mac Ds - Data/Offload/openclaw/workspace/daily-briefings"]
START = "2026-11-01"
DRY = "--dry-run" in sys.argv
ADVICE = re.compile(r"投資人|追價|追高|布局|買進|賣出|加碼|減碼|停損|進場|出場|槓桿|抄底|持股")
WEEK = "一二三四五六日"
REMOVED = f"{ROOT}/scripts/data/briefings-removed.json"
removed = set(json.load(open(REMOVED, encoding="utf-8"))) if os.path.exists(REMOVED) else set()


def news_items(text):
    m = re.search(r"^##\s*今日.*?新聞\s*$(.*?)(?=^##\s)", text, re.S | re.M)
    if not m:
        return []
    items = []
    for block in re.split(r"^###\s*", m.group(1), flags=re.M)[1:]:
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        head = re.sub(r"^\d+[.、]\s*", "", lines[0])
        body, impact = [], ""
        for l in lines[1:]:
            im = re.match(r"\*\*影響[:：]\*\*\s*(.*)", l)
            if im:
                impact = im.group(1)
            else:
                body.append(l)
        # 影響拆成句子，有操作建議的那句不放
        kept = [s for s in re.findall(r"[^；。]+[；。]?", impact) if s.strip() and not ADVICE.search(s)]
        impact = "".join(kept).strip().rstrip("；")
        if impact and not impact.endswith("。"):
            impact += "。"
        items.append({"head": head, "body": " ".join(body), "impact": impact})
    return items


def media(text):
    m = re.search(r"涵蓋([^；;。]*?)等", text)
    return m.group(1).strip() if m else ""


files = {}
for src in reversed(SOURCES):  # Drive 優先，同一天會蓋掉外接碟的
    for p in glob.glob(f"{src}/20??-??-??-morning-news.md"):
        files[os.path.basename(p)[:10]] = p

new, skipped = [], []
for date in sorted(files):
    md = f"{ROOT}/src/briefings/{date}.md"
    if date < START or date in removed or os.path.exists(md):
        continue
    try:
        text = open(files[date], encoding="utf-8").read()
    except OSError as e:
        skipped.append({"date": date, "reason": f"讀不到檔案：{e}"}); continue
    items = news_items(text)
    if len(items) < 3:
        skipped.append({"date": date, "reason": f"只解析到 {len(items)} 則新聞，格式可能改了"}); continue
    y, mo, d = map(int, date.split("-"))
    wd = WEEK[datetime.date(y, mo, d).weekday()]
    title = f"{mo}/{d}（{wd}）晨報：{items[0]['head']}"
    parts = []
    for i, it in enumerate(items, 1):
        s = f"## {i}. {it['head']}\n\n{it['body']}"
        if it["impact"]:
            s += f"\n\n**影響**：{it['impact']}"
        parts.append(s)
    src_media = media(text)
    parts.append("---\n\n" + (f"新聞整理自 {src_media} 等媒體的公開報導，" if src_media else "新聞整理自公開報導，")
                 + "由 AI 協助摘要，可能有疏漏，重要資訊請以原始報導為準。")
    fm = {"title": title, "date": date, "summary": "；".join(it["head"] for it in items)[:150]}
    if not DRY:
        os.makedirs(os.path.dirname(md), exist_ok=True)
        with open(md, "w", encoding="utf-8") as fh:
            fh.write("---json\n" + json.dumps(fm, ensure_ascii=False, indent=1) + "\n---\n" + "\n\n".join(parts) + "\n")
    new.append({"date": date, "title": title})
print(json.dumps({"new": new, "skipped": skipped}, ensure_ascii=False))
