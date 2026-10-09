#!/usr/bin/env python3
"""把 OpenClaw 寫在 Google Drive 的論文讀書報告，轉成網站的「文獻筆記」。

只新增、不覆寫：網站上已經有的論文（看 DOI 或標題）會跳過，所以重複執行也安全。
規則：
- 同一篇論文讀過好幾次，只取最完整的一份
- 不收我自己論文的筆記（src/papers/ 裡的 DOI），也不收 scripts/data/notes-removed.json 列的（刻意下架的）
- 去掉內部作業說明（選題理由、PDF 路徑、paper-inbox 等），「你」改成第一人稱
- 中文標題、分類讀報告開頭的「## 網站上架資訊」；沒寫的話用英文標題、依標題猜分類
- 作者、期刊、年份用 DOI 向 Crossref 查（結果快取在 scripts/data/crossref-cache.json）
- 讀書帳圖用 macOS 的 sips 縮成網頁大小的 JPEG

用法：python3 scripts/import_notes.py [--dry-run]
最後一行輸出 JSON：{"new": [{"slug", "title", "warning"}...]}
"""
import glob, html, json, os, re, subprocess, sys, urllib.parse, urllib.request
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "src")
CACHE = os.path.join(ROOT, "scripts", "data", "crossref-cache.json")
# 可用環境變數 NOTES_SOURCE 指到別的資料夾（測試用）
W = os.environ.get("NOTES_SOURCE") or os.path.expanduser("~/Library/CloudStorage/GoogleDrive-panda@esad.cc/我的雲端硬碟/workspace")
DIRS = ["journal-reading-reports", "journal-reading-reports 1"]
DRY = "--dry-run" in sys.argv

CATS = ["教育", "管理", "行銷", "觀光", "AI 應用", "研究方法", "理論"]
TOPIC = {"education": "教育", "management": "管理", "marketing": "行銷", "tourism": "觀光", "methods": "研究方法",
         "theory": "理論", "ai-applications": "AI 應用", "misc": None}
# 含這些字的句子是內部作業說明，不公開
INTERNAL = ["未讀", "下一篇", "資料庫", "合法保存", "去重", "paper-archive", "inbox", "/Users/", "paper-inbox", "本次未", "選題", "補給"]
OLD_FORMAT = {"Paper Structure": "論文結構", "Research Background": "研究背景", "Research Gap": "研究缺口", "Research Purpose": "研究目的",
              "Overarching Theory": "核心理論", "Literature Review": "文獻回顧", "Overview of Research Propositions or Hypotheses": "研究命題與假設",
              "Research Framework": "研究架構", "Methodology": "研究方法", "Data Analyses and Results": "資料分析與結果", "Research Findings": "研究發現",
              "Theoretical and Practical Implications": "理論與實務意涵", "Limitations and Future Research": "研究限制與未來研究"}
STOP = {"a", "an", "the", "of", "in", "on", "and", "for", "to", "with", "by", "from", "at", "as", "its", "their", "how", "do", "does", "is", "are"}

cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())[:50]


def crossref(doi):
    if doi in cache and "error" not in cache[doi]:
        return cache[doi]
    try:
        req = urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"),
                                     headers={"User-Agent": "gismo-site (mailto:panda@esad.cc)"})
        m = json.load(urllib.request.urlopen(req, timeout=20))["message"]
        cache[doi] = dict(title=html.unescape(re.sub(r"<[^>]+>", "", (m.get("title") or [""])[0])).strip(),
                          authors=", ".join(f"{a.get('given', '')} {a.get('family', '')}".strip() for a in m.get("author", [])),
                          journal=html.unescape((m.get("container-title") or [""])[0]),
                          year=((m.get("published") or m.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                          vol=m.get("volume"), issue=m.get("issue"), page=m.get("page") or m.get("article-number"))
    except Exception as e:
        cache[doi] = {"error": str(e)}
    return cache[doi]


def guess_category(title):
    t = title.lower()
    if re.search(r"touris|travel|hospitality|pilgrim|hotel|destination|nighttime", t): return "觀光"
    if re.search(r"student|educat|learning|teacher|universit|higher ed|classroom|essay|course", t): return "教育"
    if re.search(r"marketing|consumer|brand|customer|advertis|shopping|e-commerce|word-of-mouth|recommendation|purchase|influencer|kol|streamer", t): return "行銷"
    if re.search(r"hrm|human resource|leader|organi[sz]ation|team|employee|work|job|talent|career|occupation|management|firm|supply chain|entrepreneur", t): return "管理"
    if re.search(r"review|meta-analysis|scale|method|replication|simulation", t): return "研究方法"
    return "AI 應用"


def convert_old_format(s):
    """舊版 Papernote（**A. Paper Title** 粗體字母標題）轉成編號段落"""
    if "**A. Paper Title**" not in s:
        return s
    out, n = [], 0
    for blk in re.split(r"\n(?=\*\*[A-Z]\. )", s):
        m = re.match(r"\*\*[A-Z]\. ([^*]+)\*\*(?:<br>)?\s*\n?(.*)", blk, re.S)
        if not m or m.group(1).strip() == "Paper Title":
            continue
        n += 1
        body = re.sub(r"^\s*-{3,}\s*$", "", m.group(2), flags=re.M).replace("<br>", "")
        out.append(f"## {n}. {OLD_FORMAT.get(m.group(1).strip(), m.group(1).strip())}\n\n{body.strip()}")
    return "\n\n".join(out)


def website_fields(raw):
    """讀 OpenClaw 寫在開頭的「## 網站上架資訊」"""
    sec = re.search(r"^## 網站上架資訊\s*\n(.*?)(?=^#{1,2} |\Z)", raw, re.S | re.M)
    if not sec:
        return None, None
    t = re.search(r"中文標題[：:]\s*(.+)", sec.group(1))
    c = re.search(r"(?:網站)?分類[：:]\s*(.+)", sec.group(1))
    title = t.group(1).strip().strip("「」\"'*") if t else None
    cat = next((x for x in CATS if c and x.replace(" ", "") in c.group(1).replace(" ", "")), None)
    return title or None, cat


def clean_sections(s):
    keep = []
    for p in re.split(r"\n(?=#{1,3} )", "\n" + s):
        p = p.strip("\n")
        head = p.split("\n")[0]
        if not re.match(r"#{1,3} \d+\. ", head):
            continue
        body = p.split("\n", 1)[1] if "\n" in p else ""
        if re.search(r"基本(資訊|資料)", head) and sum(1 for l in body.split("\n") if l.strip().startswith("-")) >= 2:
            continue  # 只是書目清單，網頁上已有資訊框
        head = re.sub(r"^#{1,3} ", "## ", head).replace("對你研究", "對我研究").replace("對許鴻勇研究", "對我研究") \
            .replace("與使用者研究或實務可能關聯", "與我研究或實務的關聯")
        if re.search(r"啟發|整體評價|關聯", head):
            body = body.replace("許鴻勇的", "我的").replace("許鴻勇", "我").replace("你的", "我的").replace("你", "我").replace("使用者", "我")
        lines = []
        for l in body.split("\n"):
            if any(k in l for k in INTERNAL):
                l = "".join(x for x in re.split(r"(?<=[。！？])", l) if not any(k in x for k in INTERNAL))
                if not l.strip():
                    continue
            lines.append(l)
        body = re.sub(r"`([^`\n]+)`", r"\1", "\n".join(lines)).strip()
        if body:
            keep.append(head + "\n\n" + body)
    return keep


def main():
    if not os.path.isdir(W):
        print(json.dumps({"error": f"找不到 Google Drive 資料夾：{W}"}, ensure_ascii=False)); sys.exit(2)

    # 已經有的就跳過：我的論文、網站上的筆記
    skip_doi, skip_title = set(), set()
    for f in glob.glob(f"{SITE}/papers/*.md"):
        m = re.search(r"^doi: (\S+)", open(f).read(), re.M)
        m and skip_doi.add(m.group(1).lower())
    for f in glob.glob(f"{SITE}/notes/*.md"):
        t = open(f).read()
        for key, bucket in (("doi", skip_doi), ("paperTitle", skip_title)):
            m = re.search(rf'"{key}": "([^"]+)"', t)
            m and bucket.add(m.group(1).lower() if key == "doi" else norm(m.group(1)))

    # 刻意下架的筆記（DOI 或英文標題），不要再匯入
    removed = os.path.join(ROOT, "scripts", "data", "notes-removed.json")
    for x in (json.load(open(removed)) if os.path.exists(removed) else []):
        (skip_doi.add(x.lower()) if x.startswith("10.") else skip_title.add(norm(x)))

    topic_of = {}
    for d in DIRS:
        for p in glob.glob(f"{W}/{d}/by-topic/*/*.md"):
            topic_of.setdefault(os.path.basename(p), p.split("/by-topic/")[1].split("/")[0])

    groups = defaultdict(list)
    for d in DIRS:
        for f in sorted(os.listdir(f"{W}/{d}")):
            if not re.match(r"\d{4}-\d\d-\d\d_.*\.md$", f):
                continue
            raw = open(f"{W}/{d}/{f}", encoding="utf-8").read()
            s = convert_old_format(raw)
            m = re.search(r"10\.\d{4,9}/[^\s\)\]，,。>\"]+", raw)
            doi = m.group(0).lower().rstrip("*`)。.,;'\"") if m else ""
            groups[doi or norm(f[11:])].append(dict(dir=d, file=f, s=s, raw=raw, doi=doi, date=f[:10],
                                                     secs=len(re.findall(r"^#{1,3} \d+\. ", s, re.M))))

    used = {os.path.basename(f)[:-3] for f in glob.glob(f"{SITE}/notes/*.md")}
    new = []
    for key, items in sorted(groups.items(), key=lambda kv: max(i["date"] for i in kv[1])):
        if key in skip_doi or norm(items[0]["file"][11:]) in skip_title:
            continue
        best = sorted(items, key=lambda r: (r["secs"] >= 10, len(r["s"]), r["date"]), reverse=True)[0]
        doi, s, raw = best["doi"], best["s"], best["raw"]
        meta = crossref(doi) if doi and not doi.startswith("10.48550") else {}
        meta = {} if "error" in meta else meta
        h1 = re.search(r"^# (.+)$", raw, re.M)
        en_title = re.sub(r"\s+", " ", meta.get("title") or (h1.group(1).strip() if h1 else best["file"][11:-3]))
        if re.match(r"\d{4}-\d\d-\d\d", en_title):
            en_title = best["file"][11:-3]
        if norm(en_title) in skip_title:
            continue
        keep = clean_sections(s)
        if len(keep) < 5:
            print(f"略過（段落太少）：{best['file']}", file=sys.stderr); continue
        zh_title, cat = website_fields(raw)
        warning = None if zh_title else "沒有中文標題，暫用英文標題"
        rq = [k for k in keep if re.search(r"研究(問題|動機|目的)", k.split("\n")[0])] or keep
        para = next(x for x in rq[0].split("\n")[1:] if x.strip())
        para = re.sub(r"\s+", " ", re.sub(r"[*#>`]", "", para)).strip()
        slug_base = (best["date"] + "-" + "-".join([w for w in re.findall(r"[a-z0-9]+", en_title.lower()) if w not in STOP][:6]))[:80].rstrip("-")
        slug, n = slug_base, 2
        while slug in used:
            slug, n = f"{slug_base}-{n}", n + 1
        used.add(slug)
        fm = {"title": zh_title or en_title, "date": best["date"], "summary": para if len(para) <= 100 else para[:98] + "…",
              "paperTitle": en_title, "authors": meta.get("authors", ""), "year": str(meta.get("year") or ""),
              "journal": meta.get("journal", "") + (f", {meta['vol']}" if meta.get("vol") else "") + (f"({meta['issue']})" if meta.get("issue") else "") + (f", {meta['page']}" if meta.get("page") else ""),
              "doi": doi if not doi.startswith("10.48550") else "",
              "category": cat or TOPIC.get(topic_of.get(best["file"], ""), None) or guess_category(en_title)}
        if re.search(r"touris|travel|hospitality|pilgrim|hotel|destination|nighttime", en_title.lower()):
            fm["category"] = "觀光"
        if doi.startswith("10.48550"):
            fm["journal"], fm["preprint"] = "arXiv 預印本", "https://arxiv.org/abs/" + doi.split("arxiv.")[1]
        # 讀書帳圖
        m = re.search(r"\]\((reading-ledgers/[^)]+)\)", raw)
        cands = [f"{W}/{best['dir']}/" + urllib.parse.unquote(m.group(1))] if m else []
        for d in DIRS:
            cands += glob.glob(f"{W}/{d}/reading-ledgers/{glob.escape(best['file'][:-3])}*")
        src_img = next((c for c in cands if os.path.exists(c)), None)
        if not DRY:
            if src_img:
                out = f"{SITE}/files/notes/{slug}.jpg"
                subprocess.run(["sips", "-Z", "1100", "-s", "format", "jpeg", "-s", "formatOptions", "65", src_img, "--out", out], capture_output=True)
                if os.path.exists(out):
                    fm["card"] = f"/files/notes/{slug}.jpg"
            with open(f"{SITE}/notes/{slug}.md", "w") as fh:
                fh.write("---json\n" + json.dumps(fm, ensure_ascii=False, indent=1) + "\n---\n\n" + "\n\n".join(keep) + "\n")
        skip_title.add(norm(en_title))
        new.append({"slug": slug, "title": fm["title"], "warning": warning})

    if not DRY:
        json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"new": new}, ensure_ascii=False))


if __name__ == "__main__":
    main()
