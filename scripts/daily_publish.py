#!/usr/bin/env python3
"""每日審核的上架步驟：把手機審核頁上「同意」的論文與繪本匯入網站，建置檢查通過才 commit + push；「退回」的記下來不再出現。

用法：python3 scripts/daily_publish.py <decisions.json>
decisions.json：{"approved": [item...], "rejected": [item...]}，item 是審核頁 items 集合的文件（至少有 _id、key、kind、title、date，
論文另有 file，繪本另有 path；decision.title 是使用者改過的網頁標題，decision.note 是退回原因）。
最後一行輸出 JSON：{"results": [{"_id", "status": "published"|"failed"|"rejected", "url"?, "error"?}], "sha"?}
由 Claude 排程呼叫（它負責讀寫審核頁的資料庫）；Drive 的檔案要在一般 App 裡讀，所以不要用 launchd 跑。
"""
import json, os, re, subprocess, sys, tempfile
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://gismo.com.tw"
LEDGER = f"{ROOT}/scripts/data/stories-review.json"
REMOVED = f"{ROOT}/scripts/data/notes-removed.json"


def sh(*cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def rollback(paths):
    """建置或推送失敗時撤回這次匯入的檔案，下次排程才會重新匯入（否則會被當成已在網站上）"""
    paths = [p for p in paths if p != "scripts/data/crossref-cache.json"]
    if paths:
        sh("git", "checkout", "--", *[p for p in paths if sh("git", "ls-files", "--error-unmatch", p).returncode == 0])
        sh("git", "clean", "-fdq", "--", *paths)


def changed_paths():
    out = sh("git", "status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    return {l[3:].strip('"') for l in out}


def publish_paper(it):
    before = changed_paths()
    r = sh(sys.executable, "scripts/import_notes.py", "--only", it["file"], timeout=900)
    try:
        new = json.loads(r.stdout.strip().splitlines()[-1])["new"]
    except Exception:
        raise RuntimeError(f"匯入失敗：{(r.stderr or r.stdout)[-300:]}")
    if not new:
        raise RuntimeError("匯入程式沒有產生筆記（可能已在網站上，或報告已被移走）")
    slug = new[0]["slug"]
    md = f"{ROOT}/src/notes/{slug}.md"
    title = (it.get("decision") or {}).get("title")
    if title:  # 使用者在審核頁改了標題
        s = open(md, encoding="utf-8").read()
        s = re.sub(r'^ "title": "[^"]*",', ' "title": ' + json.dumps(title, ensure_ascii=False) + ",", s, count=1, flags=re.M)
        open(md, "w", encoding="utf-8").write(s)
    paths = sorted(changed_paths() - before | {f"src/notes/{slug}.md", "scripts/data/crossref-cache.json"})
    return f"{SITE}/notes/{slug}/", paths


def unique_slug(date):
    base = "story-" + date.replace("-", "")
    slug, n = base, 2
    while os.path.exists(f"{ROOT}/src/stories/{slug}.md"):
        slug, n = f"{base}-{n}", n + 1
    return slug


def publish_book(it):
    slug = unique_slug(it["date"])
    r = sh(sys.executable, "scripts/import_story.py", it["path"], slug, "--date", it["date"], timeout=1800)
    if r.returncode:
        raise RuntimeError(f"繪本匯入失敗：{(r.stderr or r.stdout)[-300:]}")
    ledger = json.load(open(LEDGER, encoding="utf-8"))
    ledger.setdefault("published", {})[os.path.basename(it["path"])] = {"slug": slug, "at": datetime.now().astimezone().isoformat(timespec="seconds"), "pushed": True}
    json.dump(ledger, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return f"{SITE}/stories/{slug}/", [f"src/stories/{slug}.md", f"src/files/stories/{slug}", "src/assets/fonts/story-bpmf.woff2", "scripts/data/stories-review.json"]


def reject(it):
    note = (it.get("decision") or {}).get("note", "")
    if it["kind"] == "paper":
        # 下架清單用 DOI（沒有就用英文標題），之後的匯入就會跳過這篇
        removed = json.load(open(REMOVED, encoding="utf-8")) if os.path.exists(REMOVED) else []
        key = it.get("doi") or it.get("paperTitle")
        if key and key not in removed:
            removed.append(key)
            json.dump(removed, open(REMOVED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return ["scripts/data/notes-removed.json"]
    ledger = json.load(open(LEDGER, encoding="utf-8"))
    ledger.setdefault("rejected", {})[os.path.basename(it["path"])] = {"reason": note, "at": datetime.now().astimezone().isoformat(timespec="seconds")}
    json.dump(ledger, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    try:  # 原因留在繪本資料夾給 Spark 看
        with open(os.path.join(it["path"], "REVIEW-REJECTED.md"), "w", encoding="utf-8") as fh:
            fh.write(f"# 審核退回（{datetime.now():%Y-%m-%d %H:%M}）\n\n{note}\n")
    except OSError:
        pass
    return ["scripts/data/stories-review.json"]


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    sh("git", "pull", "--rebase", "--autostash", "-q")
    results, paths, titles = [], set(), []
    for it in d.get("rejected", []):
        paths |= set(reject(it))
        results.append({"_id": it["_id"], "status": "rejected"})
    for it in d.get("approved", []):
        try:
            url, p = (publish_paper if it["kind"] == "paper" else publish_book)(it)
            paths |= set(p)
            titles.append((it.get("decision") or {}).get("title") or it["title"])
            results.append({"_id": it["_id"], "status": "published", "url": url})
        except Exception as e:
            results.append({"_id": it["_id"], "status": "failed", "error": str(e)[:300]})
    out = {"results": results}
    if paths:
        with tempfile.TemporaryDirectory() as tmp:  # 整個網站建置得起來才推
            b = sh("npx", "--no-install", "eleventy", f"--output={tmp}", timeout=600)
        if b.returncode:
            for r in results:
                if r["status"] == "published":
                    r.update(status="failed", error="網站建置失敗，這次沒有推上去：" + (b.stderr or b.stdout)[-200:])
            rollback(sorted(paths))
            print(json.dumps(out, ensure_ascii=False)); return
        paths = sorted(p for p in paths if os.path.exists(f"{ROOT}/{p}"))
        sh("git", "add", "--", *paths)
        msg = ("審核上架：" + "、".join(titles)) if titles else "審核退回紀錄更新"
        c = sh("git", "commit", "-q", "-m", msg, "--", *paths)
        p = sh("git", "push", "-q") if c.returncode == 0 else c
        if p.returncode:
            for r in results:
                if r["status"] == "published":
                    r.update(status="failed", error="git commit／push 失敗：" + (p.stderr or p.stdout)[-200:])
            if c.returncode == 0:
                sh("git", "reset", "-q", "--soft", "HEAD~1")  # 還沒推出去的 commit 撤回
            sh("git", "reset", "-q", "--", *paths)
            rollback(paths)
        else:
            out["sha"] = sh("git", "log", "-1", "--format=%h").stdout.strip()
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
