#!/usr/bin/env python3
"""每日審核：找出 Spark／OpenClaw 產出、還沒上架的論文與繪本，加上當天早報，輸出成一份 JSON。

用法：python3 scripts/review_queue.py [--thumbs 縮圖資料夾]
- 論文：用 import_notes.py --dry-run 找出可上架的新報告（含網頁內文預覽）
- 繪本：Google Drive「睡前故事繪本」＋外接碟 OpenClaw picturebooks；跳過網站已有、stories-review.json 已上架／已退回、使用者說不要的
  自動檢查頁數、分鏡對應、SVG 假圖、鏡頭種類；--thumbs 時每個不同的圖做一張 360px JPEG 縮圖（給手機審核頁）
- 早報：Drive workspace/daily-briefings 最新一份（只供閱讀，不上網站）
每一項都有穩定的 id（paper:<報告檔名>、book:<資料夾名>、brief:<日期>），審核頁用它記錄同意／退回。
Drive 的檔案要在一般 App 裡讀（launchd 背景讀會出 Errno 11），所以由 Claude 排程執行。
"""
import glob, hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVE = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-panda@esad.cc/我的雲端硬碟")
BOOK_DIRS = [f"{DRIVE}/睡前故事繪本", "/Volumes/mac Ds - Data/Offload/openclaw/workspace/bedtime-story/picturebooks"]
BRIEFS = f"{DRIVE}/workspace/daily-briefings"
NEVER = ["雲杉林裡小貘的靜靜風箏", "星霧果園裡小鸚鵡的晚安果籃"]  # 使用者說品質不好（CLAUDE.md）
THUMBS = sys.argv[sys.argv.index("--thumbs") + 1] if "--thumbs" in sys.argv else None

md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()


def papers():
    r = subprocess.run([sys.executable, f"{ROOT}/scripts/import_notes.py", "--dry-run"], capture_output=True, text=True, timeout=900)
    skipped = [l.split("：", 1)[1] for l in r.stderr.splitlines() if l.startswith("略過")]
    try:
        new = json.loads(r.stdout.strip().splitlines()[-1])["new"]
    except Exception:
        return [], [f"論文掃描失敗：{(r.stderr or r.stdout)[-300:]}"]
    out = []
    for n in new:
        fm = n["fm"]
        out.append({"id": f"paper:{n['file']}", "kind": "paper", "date": fm["date"], "title": fm["title"],
                    "paperTitle": fm["paperTitle"], "authors": fm["authors"], "journal": fm["journal"], "year": fm["year"],
                    "doi": fm["doi"], "category": fm["category"], "summary": fm["summary"], "body": n["body"],
                    "warning": n["warning"], "file": n["file"]})
    return out, [f"論文報告格式無法匯入：{s}" for s in skipped]


def site_titles():
    titles = set()
    for f in glob.glob(f"{ROOT}/src/stories/*.md"):
        m = re.search(r'"title": "([^"]+)"', open(f, encoding="utf-8").read())
        m and titles.add(m.group(1))
    return titles


def inspect_book(d):
    has = lambda p: os.path.exists(f"{d}/{p}")
    ls = lambda sub, rx: sorted(f for f in os.listdir(f"{d}/{sub}") if re.match(rx, f)) if os.path.isdir(f"{d}/{sub}") else []
    texts = [t.strip() for t in open(f"{d}/narration-pages.txt", encoding="utf-8").read().split("\n\n") if t.strip()]
    illus, audio = ls("images", r"illustration-\d+\.png$"), ls("audio", r"page-\d+\.m4a$")
    caps = len([l for l in open(f"{d}/captions-zhuyin.txt", encoding="utf-8").read().splitlines() if l]) if has("captions-zhuyin.txt") else 0
    mp4 = next((f for f in os.listdir(d) if "有聲繪本" in f and f.endswith(".mp4")), None)
    n, checks = len(texts), []
    ok = lambda p, label, detail="": checks.append({"pass": bool(p), "label": label, "detail": detail})
    ok(mp4 and has("flipbook-reader.html"), "收尾完成", "" if mp4 else "缺 MP4 或翻頁網頁")
    ok(n and len(illus) == n == len(audio) == caps, "頁數一致", f"頁 {n}／圖 {len(illus)}／音 {len(audio)}／字幕 {caps}")
    ok(not ls("images", r".*\.svg$") and not any(f.lower().endswith(".svg") for f in os.listdir(d)), "沒有 SVG 替代圖")
    shots = []
    if has("storyboard.json"):
        scenes = json.load(open(f"{d}/storyboard.json", encoding="utf-8")).get("scenes", [])
        pages = [p for s in scenes for p in s["pages"]]
        ok(pages == list(range(1, n + 1)), "分鏡頁碼完整", f"{len(scenes)} 個場景涵蓋 {len(pages)} 頁")
        # 同一場景的幾頁要是同一張圖、不同場景要不同（Spark 版沒有另存 scene-NN.png，只比對每頁的插圖）
        bad, scene_hash = [], {}
        for s in scenes:
            hs = {md5(f"{d}/images/illustration-{p:02}.png") for p in s["pages"] if os.path.exists(f"{d}/images/illustration-{p:02}.png")}
            src = f"{d}/images/scene-{s['id']:02}.png"
            if os.path.exists(src):
                hs.add(md5(src))
            if len(hs) != 1:
                bad.append(f"場景 {s['id']}（第 {s['pages'][0]}～{s['pages'][-1]} 頁）圖不一致")
            else:
                scene_hash[s["id"]] = hs.pop()
        dup = len(scene_hash) - len(set(scene_hash.values()))
        dup and bad.append(f"{dup} 個場景用了重複的圖")
        ok(not bad, "每頁的圖對上分鏡", "、".join(bad[:6]))
        shots = sorted({s.get("shot") for s in scenes if s.get("shot")})
        ok(len(shots) >= 4, "鏡頭種類 ≥ 4", f"{len(shots)} 種")
    else:
        ok(False, "有分鏡表", "沒有 storyboard.json")
    # 每張不同的圖第一次出現在哪一頁
    first, seen = [], set()
    for i, f in enumerate(illus, 1):
        h = md5(f"{d}/images/{f}")
        if h not in seen:
            seen.add(h); first.append(i)
    ok(len(seen) >= min(n, 6), "插圖有變化", f"{len(seen)} 張不同的圖")
    return texts, checks, first, shots


def books(skip_titles):
    ledger = json.load(open(f"{ROOT}/scripts/data/stories-review.json"))
    done = set(ledger.get("published", {})) | set(ledger.get("rejected", {}))
    out, seen_titles = [], set()
    for base in BOOK_DIRS:
        if not os.path.isdir(base):
            continue
        for folder in sorted(os.listdir(base), reverse=True):
            d = f"{base}/{folder}"
            m = re.match(r"(\d{4}-\d\d-\d\d)-(.+)$", folder)
            if not m or not os.path.isdir(d) or "樣本" in folder or folder in done:
                continue
            title = re.sub(r"-(v\d+|完整)$", "", m.group(2))
            if title in NEVER or title in skip_titles or title in seen_titles or not os.path.exists(f"{d}/narration-pages.txt"):
                continue
            seen_titles.add(title)
            texts, checks, first, shots = inspect_book(d)
            item = {"id": f"book:{folder}", "kind": "book", "date": m.group(1), "title": title, "path": d,
                    "pages": len(texts), "texts": texts, "checks": checks, "passed": all(c["pass"] for c in checks),
                    "shots": shots, "thumbPages": first}
            if THUMBS:
                os.makedirs(THUMBS, exist_ok=True)
                item["thumbs"] = []
                for p in first[:12]:
                    t = f"{THUMBS}/{hashlib.md5(folder.encode()).hexdigest()[:10]}-p{p:02}.jpg"
                    if not os.path.exists(t):
                        subprocess.run(["sips", "-Z", "360", "-s", "format", "jpeg", "-s", "formatOptions", "70",
                                        f"{d}/images/illustration-{p:02}.png", "--out", t], capture_output=True)
                    os.path.exists(t) and item["thumbs"].append({"page": p, "file": t})
            out.append(item)
    return out


def brief():
    files = sorted(glob.glob(f"{BRIEFS}/*-morning-news.md"))
    if not files:
        return None
    f = files[-1]
    return {"id": f"brief:{os.path.basename(f)[:10]}", "kind": "brief", "date": os.path.basename(f)[:10],
            "title": "每日晨報", "body": open(f, encoding="utf-8").read()}


if __name__ == "__main__":
    p, notes = papers()
    out = {"papers": p, "books": books(site_titles()), "brief": brief(), "notes": notes}
    # 審核頁資料庫的文件 id（固定、不含 / 等特殊字元）：同一項目每天掃到都是同一個 id，已存在就不重複加入
    for it in out["papers"] + out["books"]:
        it["docId"] = it["kind"][0] + "-" + hashlib.md5(it["id"].encode()).hexdigest()[:16]
    print(json.dumps(out, ensure_ascii=False))
