#!/bin/bash
# 每天自動上架文獻筆記：匯入 Google Drive 新的讀書報告 → 確認網站能建置 → 只提交筆記 → 推上 GitHub
# 由 ~/Library/LaunchAgents/tw.gismo.publish-notes.plist 每天 13:00 執行；紀錄在 ~/Library/Logs/gismo-publish-notes.log
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
cd "$(dirname "$0")/.."

notify() { osascript -e "display notification \"$2\" with title \"勇博講古\" subtitle \"$1\"" >/dev/null 2>&1; }
fail() { echo "失敗：$1"; notify "文獻筆記上架失敗" "$1"; exit 1; }

echo "=== $(date '+%Y-%m-%d %H:%M') 開始"
git pull --rebase --autostash -q || fail "git pull 失敗"

result=$(python3 scripts/import_notes.py) || fail "匯入程式出錯"
echo "$result"
count=$(echo "$result" | tail -1 | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('new', [])))")
[ "$count" = "0" ] && { echo "沒有新筆記"; exit 0; }

# 先確認整個網站還能正常建置，才推上去
tmp=$(mktemp -d)
npx --no-install eleventy --output="$tmp" >/dev/null 2>&1 || { git checkout -- src/notes src/files/notes 2>/dev/null; git clean -fdq src/notes src/files/notes; rm -rf "$tmp"; fail "網站建置失敗，已撤回"; }
rm -rf "$tmp"

titles=$(echo "$result" | tail -1 | python3 -c "import json,sys; print('、'.join(n['title'] for n in json.load(sys.stdin)['new']))")
git add src/notes src/files/notes scripts/data/crossref-cache.json
git commit -q -m "自動上架文獻筆記 ${count} 篇：${titles}" -- src/notes src/files/notes scripts/data/crossref-cache.json || fail "git commit 失敗"
git push -q || fail "git push 失敗"

warn=$(echo "$result" | tail -1 | python3 -c "import json,sys; w=[n['title'] for n in json.load(sys.stdin)['new'] if n.get('warning')]; print('（缺中文標題：' + '、'.join(w) + '）' if w else '')")
echo "完成：${count} 篇 ${warn}"
notify "文獻筆記已上架 ${count} 篇" "${titles}${warn}"
