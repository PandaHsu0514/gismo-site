// Google Analytics（GA4）：只在正式網站載入，本機預覽不送資料
// 遊戲可以呼叫 track("事件名稱", { 參數 }) 記錄遊玩行為（不含個人資料）
(function () {
  var ID = "G-QGX3E2W1GM"; // 與 src/_data/site.json 的 ga 相同
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { dataLayer.push(arguments); };
  window.track = function (name, params) { try { gtag("event", name, params || {}); } catch (e) {} };
  if (!/(^|\.)gismo\.com\.tw$/.test(location.hostname)) return;
  var s = document.createElement("script");
  s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID;
  document.head.appendChild(s);
  gtag("js", new Date());
  gtag("config", ID, { allow_google_signals: false, allow_ad_personalization_signals: false });
})();
