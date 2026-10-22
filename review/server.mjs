// 本機審核台：列出 OpenClaw 做好、還沒上架的有聲繪本，核准後匯入網站，再由使用者按「推上網站」commit + push。
// 用法：npm run review（只聽 127.0.0.1，網址帶隨機 token；不會被建置進網站）
// 測試時可用環境變數 REVIEW_PICTUREBOOKS 指到別的繪本資料夾、REVIEW_PORT 換埠號。
import { createServer } from "node:http";
import { createHash, randomBytes } from "node:crypto";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const run = promisify(execFile);
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const BOOKS = process.env.REVIEW_PICTUREBOOKS || "/Volumes/mac Ds - Data/Offload/openclaw/workspace/bedtime-story/picturebooks";
const LEDGER = path.join(ROOT, "scripts/data/stories-review.json");
const PORT = Number(process.env.REVIEW_PORT || 8090);
const TOKEN = randomBytes(12).toString("hex");
const THUMBS = fs.mkdtempSync(path.join(os.tmpdir(), "review-thumbs-"));
// 使用者說品質不好、不要放的（CLAUDE.md）
const NEVER = ["雲杉林裡小貘的靜靜風箏", "星霧果園裡小鸚鵡的晚安果籃"];

const readJSON = (f, d) => { try { return JSON.parse(fs.readFileSync(f, "utf8")); } catch { return d; } };
const ledger = () => readJSON(LEDGER, { published: {}, rejected: {} });
const saveLedger = (l) => fs.writeFileSync(LEDGER, JSON.stringify(l, null, 1) + "\n");
const md5 = (f) => createHash("md5").update(fs.readFileSync(f)).digest("hex");
const titleOf = (folder) => folder.replace(/^\d{4}-\d\d-\d\d-/, "");

// 網站上已經有的故事標題
function siteTitles() {
  const dir = path.join(ROOT, "src/stories");
  return new Set(fs.readdirSync(dir).filter((f) => f.endsWith(".md")).map((f) => {
    const m = fs.readFileSync(path.join(dir, f), "utf8").match(/"title": "([^"]+)"/);
    return m && m[1];
  }));
}

// 一本書的檢查結果
function inspect(folder) {
  const dir = path.join(BOOKS, folder);
  const has = (p) => fs.existsSync(path.join(dir, p));
  const list = (sub, re) => (fs.existsSync(path.join(dir, sub)) ? fs.readdirSync(path.join(dir, sub)).filter((f) => re.test(f)).sort() : []);
  const texts = has("narration-pages.txt") ? fs.readFileSync(path.join(dir, "narration-pages.txt"), "utf8").split("\n\n").map((s) => s.trim()).filter(Boolean) : [];
  const illus = list("images", /^illustration-\d+\.png$/);
  const audio = list("audio", /^page-\d+\.m4a$/);
  const caps = has("captions-zhuyin.txt") ? fs.readFileSync(path.join(dir, "captions-zhuyin.txt"), "utf8").split("\n").filter(Boolean).length : 0;
  const mp4 = fs.readdirSync(dir).find((f) => f.includes("有聲繪本") && f.endsWith(".mp4"));
  const story = readJSON(path.join(dir, "storyboard.json"), null);
  const checks = [];
  const ok = (pass, label, detail = "") => checks.push({ pass, label, detail });
  const n = texts.length;
  ok(Boolean(mp4) && has("flipbook-reader.html"), "收尾完成", mp4 ? "" : "缺 MP4 或翻頁網頁（finish_picturebook.sh 沒跑完）");
  ok(n > 0 && illus.length === n && audio.length === n && caps === n, "頁數一致", `頁 ${n}／圖 ${illus.length}／音 ${audio.length}／字幕 ${caps}`);
  ok(!list("images", /\.svg$/i).length && !fs.readdirSync(dir).some((f) => /\.svg$/i.test(f)), "沒有 SVG 替代圖");
  let scenes = [];
  if (story && Array.isArray(story.scenes)) {
    scenes = story.scenes;
    const pages = scenes.flatMap((s) => s.pages);
    ok(pages.join() === Array.from({ length: n }, (_, i) => i + 1).join(), "分鏡頁碼完整", `${scenes.length} 個場景涵蓋 ${pages.length} 頁`);
    const bad = [];
    for (const s of scenes) {
      const src = path.join(dir, "images", `scene-${String(s.id).padStart(2, "0")}.png`);
      if (!fs.existsSync(src)) { bad.push(`缺 scene-${s.id}`); continue; }
      const h = md5(src);
      for (const p of s.pages) {
        const f = path.join(dir, "images", `illustration-${String(p).padStart(2, "0")}.png`);
        if (!fs.existsSync(f) || md5(f) !== h) bad.push(`第 ${p} 頁`);
      }
    }
    ok(!bad.length, "每頁的圖對上分鏡", bad.slice(0, 8).join("、"));
    const shots = new Set(scenes.map((s) => s.shot).filter(Boolean));
    ok(shots.size >= 4, "鏡頭種類 ≥ 4", `${shots.size} 種：${[...shots].join("、")}`);
  } else {
    ok(false, "有分鏡表", "沒有 storyboard.json：可能是每句一張圖、構圖容易重複");
  }
  const uniq = new Set(illus.map((f) => md5(path.join(dir, "images", f)))).size;
  ok(n === 0 || uniq >= Math.min(n, 6), "插圖有變化", `${uniq} 張不同的圖`);
  ok(["start", "middle", "end"].every((k) => has(`.verify/${k}.png`)), "MP4 影格已抽查", "");
  // 給畫面用：每張不同的圖第一次出現在第幾頁
  const firstPage = [];
  const seen = new Set();
  illus.forEach((f, i) => { const h = md5(path.join(dir, "images", f)); if (!seen.has(h)) { seen.add(h); firstPage.push(i + 1); } });
  return { folder, title: titleOf(folder), date: folder.slice(0, 10), pages: n, texts, checks, passed: checks.every((c) => c.pass), scenes: firstPage, mp4 };
}

function queue() {
  const l = ledger(), onSite = siteTitles();
  const out = { pending: [], published: [], rejected: [] };
  if (!fs.existsSync(BOOKS)) return { error: `找不到繪本資料夾（外接碟沒接上？）：${BOOKS}`, ...out };
  for (const folder of fs.readdirSync(BOOKS).sort().reverse()) {
    if (folder.startsWith(".") || folder.startsWith("_") || !/^\d{4}-\d\d-\d\d-/.test(folder)) continue;
    const dir = path.join(BOOKS, folder);
    if (!fs.statSync(dir).isDirectory() || folder.includes("樣本")) continue;
    const title = titleOf(folder).replace(/-(v\d+|完整)$/, "");
    if (NEVER.includes(title)) continue;
    if (!fs.existsSync(path.join(dir, "narration-pages.txt"))) continue; // 還沒做到收尾
    const item = { folder, title, date: folder.slice(0, 10) };
    if (l.rejected[folder]) out.rejected.push({ ...item, reason: l.rejected[folder].reason });
    else if (l.published[folder] || onSite.has(title)) out.published.push({ ...item, slug: l.published[folder]?.slug, unpushed: l.published[folder] ? !l.published[folder].pushed : false });
    else out.pending.push({ ...inspect(folder), title });
  }
  return out;
}

const changedFiles = async () => (await run("git", ["status", "--porcelain", "--", "src/stories", "src/files/stories", "src/assets/fonts", "scripts/data/stories-review.json"], { cwd: ROOT })).stdout.trim().split("\n").filter(Boolean);

async function approve({ folder, slug }) {
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug || "")) throw new Error("網址代稱只能用小寫英文、數字和 -");
  const item = queue().pending.find((p) => p.folder === folder);
  if (!item) throw new Error("清單裡沒有這本（可能已處理）");
  if (!item.passed) throw new Error("自動檢查沒全過，不能核准");
  await run("python3", [path.join(ROOT, "scripts/import_story.py"), path.join(BOOKS, folder), slug, "--date", item.date], { cwd: ROOT, maxBuffer: 1 << 24 });
  const tmp = fs.mkdtempSync("/tmp/review-build-");
  try { await run("npx", ["--no-install", "eleventy", `--output=${tmp}`], { cwd: ROOT, maxBuffer: 1 << 24 }); }
  catch (e) { throw new Error("網站建置失敗，請檢查：" + e.message.slice(0, 300)); }
  finally { fs.rmSync(tmp, { recursive: true, force: true }); }
  const l = ledger(); l.published[folder] = { slug, at: new Date().toISOString(), pushed: false }; saveLedger(l);
  return { slug, files: await changedFiles(), preview: `http://localhost:8080/stories/${slug}/` };
}

// 核准後、推上去之前反悔：刪掉這次匯入產生的檔案（都還沒進 git），重產字型
async function unapprove({ folder }) {
  const l = ledger(), v = l.published[folder];
  if (!v || v.pushed) throw new Error("只能撤銷還沒推上去的核准");
  fs.rmSync(path.join(ROOT, "src/stories", `${v.slug}.md`), { force: true });
  fs.rmSync(path.join(ROOT, "src/files/stories", v.slug), { recursive: true, force: true });
  delete l.published[folder]; saveLedger(l);
  await run("python3", [path.join(ROOT, "scripts/build_story_font.py")], { cwd: ROOT });
  return { ok: true };
}

async function reject({ folder, reason }) {
  if (!reason || !reason.trim()) throw new Error("請寫退回原因");
  const l = ledger(); l.rejected[folder] = { reason: reason.trim(), at: new Date().toISOString() }; saveLedger(l);
  // 留一份給 OpenClaw 看
  fs.writeFileSync(path.join(BOOKS, folder, "REVIEW-REJECTED.md"), `# 審核退回（${new Date().toLocaleString("zh-TW")}）\n\n${reason.trim()}\n`);
  return { ok: true };
}

async function publish() {
  const l = ledger();
  const items = Object.entries(l.published).filter(([, v]) => !v.pushed);
  if (!items.length) throw new Error("沒有已核准、還沒推上去的繪本");
  const paths = ["src/assets/fonts/story-bpmf.woff2", "scripts/data/stories-review.json"];
  for (const [, v] of items) paths.push(`src/stories/${v.slug}.md`, `src/files/stories/${v.slug}`);
  for (const [, v] of items) v.pushed = true;
  saveLedger(l);
  const titles = items.map(([f]) => titleOf(f)).join("、");
  await run("git", ["pull", "--rebase", "--autostash", "-q"], { cwd: ROOT });
  await run("git", ["add", "--", ...paths], { cwd: ROOT });
  await run("git", ["commit", "-q", "-m", `新增晚安故事：${titles}（審核台核准）`, "--", ...paths], { cwd: ROOT });
  await run("git", ["push", "-q"], { cwd: ROOT });
  const sha = (await run("git", ["log", "-1", "--format=%h"], { cwd: ROOT })).stdout.trim();
  return { sha, titles, urls: items.map(([, v]) => `https://gismo.com.tw/stories/${v.slug}/`) };
}

const TYPES = { ".png": "image/png", ".jpg": "image/jpeg", ".m4a": "audio/mp4", ".mp4": "video/mp4", ".html": "text/html; charset=utf-8", ".ttf": "font/ttf", ".css": "text/css", ".js": "text/javascript" };

createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const send = (code, body, type = "application/json; charset=utf-8") => { res.writeHead(code, { "content-type": type, "cache-control": "no-store" }); res.end(type.startsWith("application/json") ? JSON.stringify(body) : body); };
  // 只接受本機、帶 token 的請求（cookie 或網址參數）
  const cookieTok = (req.headers.cookie || "").match(/rv=([0-9a-f]+)/)?.[1];
  if (url.searchParams.get("t") === TOKEN) { res.setHeader("set-cookie", `rv=${TOKEN}; HttpOnly; SameSite=Strict; Path=/`); }
  else if (cookieTok !== TOKEN) return send(403, "請用啟動時印出的網址開啟", "text/plain; charset=utf-8");
  try {
    if (url.pathname === "/") return send(200, fs.readFileSync(path.join(ROOT, "review/index.html")), "text/html; charset=utf-8");
    if (url.pathname === "/api/queue") return send(200, queue());
    if (req.method === "POST" && url.pathname.startsWith("/api/")) {
      if (req.headers["sec-fetch-site"] && req.headers["sec-fetch-site"] !== "same-origin") return send(403, { error: "拒絕跨站請求" });
      let raw = ""; for await (const c of req) raw += c;
      const body = raw ? JSON.parse(raw) : {};
      const fn = { "/api/approve": approve, "/api/unapprove": unapprove, "/api/reject": reject, "/api/publish": publish }[url.pathname];
      if (!fn) return send(404, { error: "沒有這個動作" });
      return send(200, await fn(body));
    }
    // 繪本檔案：/book/<資料夾>/<路徑>（/thumb/ 是縮圖），不准跳出資料夾
    if (url.pathname.startsWith("/book/") || url.pathname.startsWith("/thumb/")) {
      const thumb = url.pathname.startsWith("/thumb/");
      const [folder, ...rest] = decodeURIComponent(url.pathname.slice(thumb ? 7 : 6)).split("/");
      const base = path.join(BOOKS, folder);
      let file = path.resolve(base, ...rest);
      if (!file.startsWith(base + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return send(404, "not found", "text/plain");
      if (thumb) {
        // 原圖約 3 MB、又在外接碟，縮成 360px JPEG 暫存起來
        const cached = path.join(THUMBS, createHash("md5").update(file + fs.statSync(file).mtimeMs).digest("hex") + ".jpg");
        if (!fs.existsSync(cached)) await run("sips", ["-Z", "360", "-s", "format", "jpeg", file, "--out", cached]);
        file = cached;
      }
      res.writeHead(200, { "content-type": TYPES[path.extname(file).toLowerCase()] || "application/octet-stream", "cache-control": "no-store" });
      return fs.createReadStream(file).pipe(res);
    }
    send(404, "not found", "text/plain");
  } catch (e) { send(400, { error: e.message }); }
}).listen(PORT, "127.0.0.1", () => {
  const link = `http://127.0.0.1:${PORT}/?t=${TOKEN}`;
  console.log(`審核台：${link}`);
  if (!process.env.REVIEW_NO_OPEN) execFile("open", [link]);
});
