// 所有小遊戲共用的小工具：顏色、分數、開始／結束畫面、主迴圈、鍵盤、觸控
(function () {
  var K = (window.K = {});
  var css = getComputedStyle(document.documentElement);
  K.c = function (name) { return css.getPropertyValue("--" + name).trim(); };
  K.$ = function (id) { return document.getElementById(id); };
  K.rand = function (a, b) { return a + Math.random() * (b - a); };
  K.ri = function (a, b) { return Math.floor(a + Math.random() * (b - a + 1)); };
  K.pick = function (arr) { return arr[Math.floor(Math.random() * arr.length)]; };
  K.shuffle = function (a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.random() * (i + 1) | 0, t = a[i]; a[i] = a[j]; a[j] = t; } return a; };
  K.hit = function (a, b) { return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; };
  K.clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };

  // 分數與最高紀錄（存在瀏覽器）。low: true 代表數字越小越好（例如秒數、步數）
  K.hud = function (key, opts) {
    opts = opts || {};
    var best = 0, scoreEl = K.$("score"), bestEl = K.$("best");
    try { best = +localStorage.getItem(key) || 0; } catch (e) {}
    var fmt = opts.fmt || String;
    if (bestEl) bestEl.textContent = best ? fmt(best) : (opts.low ? "—" : "0");
    return {
      set: function (n) { if (scoreEl) scoreEl.textContent = fmt(n); },
      get best() { return best; },
      finish: function (n) {
        var better = opts.low ? (n > 0 && (!best || n < best)) : n > best;
        if (better) { best = n; if (bestEl) bestEl.textContent = fmt(n); try { localStorage.setItem(key, n); } catch (e) {} }
        return better;
      }
    };
  };

  // 疊在畫面上的訊息卡片
  K.show = function (title, msg, label, onClick) {
    var ov = K.$("ov");
    ov.innerHTML = '<div class="card"><h2></h2><p></p><button type="button"></button></div>';
    ov.querySelector("h2").textContent = title;
    ov.querySelector("p").textContent = msg || "";
    var b = ov.querySelector("button");
    b.textContent = label || "開始";
    b.onclick = function () { K.hide(); onClick && onClick(); };
    ov.hidden = false;
    setTimeout(function () { b.focus(); }, 0);
  };
  K.hide = function () { K.$("ov").hidden = true; };

  // 主迴圈：fn(dt) 每格呼叫，dt 是秒；分頁切走時自動暫停
  K.loop = function (fn) {
    var last = 0, id = 0, run = true;
    function f(t) { if (!run) return; var dt = last ? Math.min((t - last) / 1000, 0.05) : 0; last = t; fn(dt); id = requestAnimationFrame(f); }
    id = requestAnimationFrame(f);
    return { stop: function () { run = false; cancelAnimationFrame(id); } };
  };

  // 按住中的按鍵
  K.keys = {};
  var block = { ArrowUp: 1, ArrowDown: 1, ArrowLeft: 1, ArrowRight: 1, " ": 1 };
  addEventListener("keydown", function (e) { K.keys[e.key.length === 1 ? e.key.toLowerCase() : e.key] = true; if (block[e.key] && e.target.tagName !== "BUTTON") e.preventDefault(); });
  addEventListener("keyup", function (e) { K.keys[e.key.length === 1 ? e.key.toLowerCase() : e.key] = false; });
  addEventListener("blur", function () { K.keys = {}; });
  K.left = function () { return K.keys.ArrowLeft || K.keys.a; };
  K.right = function () { return K.keys.ArrowRight || K.keys.d; };
  K.up = function () { return K.keys.ArrowUp || K.keys.w; };
  K.down = function () { return K.keys.ArrowDown || K.keys.s; };

  // 觸控按鈕：<div class="pad" id="pad"></div>，按住等於按住鍵盤上的 key
  K.pad = function (buttons) {
    var pad = K.$("pad");
    buttons.forEach(function (b) {
      var el = document.createElement("button"); el.type = "button"; el.textContent = b[0];
      var key = b[1];
      function down(e) { e.preventDefault(); K.keys[key] = true; el.classList.add("on"); dispatchEvent(new KeyboardEvent("keydown", { key: key })); }
      function up(e) { e.preventDefault(); K.keys[key] = false; el.classList.remove("on"); }
      el.addEventListener("pointerdown", down); el.addEventListener("pointerup", up);
      el.addEventListener("pointerleave", up); el.addEventListener("pointercancel", up);
      pad.appendChild(el);
    });
  };

  // 畫布上的指標（滑鼠或手指），座標換算成畫布座標
  K.pointer = function (cv) {
    var p = { x: cv.width / 2, y: cv.height / 2, down: false, active: false, onDown: null, onUp: null };
    function pos(e) { var r = cv.getBoundingClientRect(); p.x = (e.clientX - r.left) * cv.width / r.width; p.y = (e.clientY - r.top) * cv.height / r.height; }
    cv.addEventListener("pointerdown", function (e) { pos(e); p.down = p.active = true; try { cv.setPointerCapture(e.pointerId); } catch (err) {} p.onDown && p.onDown(p, e); });
    cv.addEventListener("pointermove", function (e) { pos(e); p.active = true; });
    cv.addEventListener("pointerup", function (e) { pos(e); p.down = false; p.onUp && p.onUp(p, e); });
    cv.addEventListener("pointercancel", function () { p.down = false; });
    return p;
  };

  // 滑動手勢：fn("up" | "down" | "left" | "right")
  K.swipe = function (el, fn) {
    var s = null;
    el.addEventListener("pointerdown", function (e) { s = { x: e.clientX, y: e.clientY }; });
    el.addEventListener("pointerup", function (e) {
      if (!s) return; var dx = e.clientX - s.x, dy = e.clientY - s.y; s = null;
      if (Math.max(Math.abs(dx), Math.abs(dy)) < 24) return;
      fn(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up"));
    });
    el.style.touchAction = "none";
  };

  // 簡單音效
  var ac;
  K.beep = function (freq, dur, type, vol) {
    try {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)();
      var o = ac.createOscillator(), g = ac.createGain();
      o.type = type || "sine"; o.frequency.value = freq; g.gain.value = vol || 0.08;
      g.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime + (dur || 0.12));
      o.connect(g); g.connect(ac.destination); o.start(); o.stop(ac.currentTime + (dur || 0.12));
    } catch (e) {}
  };
})();
