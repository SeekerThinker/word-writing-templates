(() => {
  "use strict";

  const KEY = "word-writing-templates-language";
  const html = document.documentElement;
  const current = (html.lang || "zh-CN").toLowerCase().startsWith("en") ? "en" : "zh";
  const path = window.location.pathname;
  const isGuide = /\/guide\.html$/.test(path);

  function withQueryAndHash(target) {
    return `${target}${window.location.search}${window.location.hash}`;
  }

  function targetFor(lang) {
    if (current === "zh" && lang === "en") {
      return withQueryAndHash(isGuide ? "./en/guide.html" : "./en/");
    }
    if (current === "en" && lang === "zh") {
      return withQueryAndHash(isGuide ? "../guide.html" : "../");
    }
    return window.location.href;
  }

  function preferredLanguage() {
    try {
      const saved = localStorage.getItem(KEY);
      if (saved === "zh" || saved === "en") return saved;
    } catch (_) {}
    const candidates = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ""];
    return candidates.some((item) => /^zh(?:-|$)/i.test(item)) ? "zh" : "en";
  }

  function remember(lang) {
    try { localStorage.setItem(KEY, lang); } catch (_) {}
  }

  if (current === "zh" && preferredLanguage() === "en") {
    window.location.replace(targetFor("en"));
    return;
  }

  const topbar = document.querySelector(".topbar");
  if (!topbar) return;

  const style = document.createElement("style");
  style.textContent = `
    .language-switch {
      display: inline-flex;
      align-items: center;
      gap: 2px;
      margin-left: auto;
      padding: 3px;
      border: 1px solid var(--line, #dedbd1);
      border-radius: 999px;
      background: rgba(255,255,255,.45);
      font-size: 12px;
      line-height: 1;
    }
    .language-switch a {
      padding: 7px 9px;
      border-radius: 999px;
      color: var(--muted, #696a62);
      text-decoration: none;
      white-space: nowrap;
    }
    .language-switch a[aria-current="true"] {
      background: var(--accent-soft, #e6eee9);
      color: var(--accent, #2d5a4a);
      font-weight: 800;
    }
    .topbar .language-switch + .top-link { margin-left: 8px; }
    @media (max-width: 600px) {
      .language-switch { margin-left: auto; }
      .language-switch a { padding: 6px 8px; }
    }
  `;
  document.head.appendChild(style);

  const wrap = document.createElement("nav");
  wrap.className = "language-switch";
  wrap.setAttribute("aria-label", current === "en" ? "Language" : "语言");

  const zh = document.createElement("a");
  zh.href = targetFor("zh");
  zh.textContent = "中文";
  zh.setAttribute("lang", "zh-CN");
  zh.setAttribute("aria-current", current === "zh" ? "true" : "false");
  zh.addEventListener("click", () => remember("zh"));

  const en = document.createElement("a");
  en.href = targetFor("en");
  en.textContent = "EN";
  en.setAttribute("lang", "en");
  en.setAttribute("aria-current", current === "en" ? "true" : "false");
  en.addEventListener("click", () => remember("en"));

  wrap.append(zh, en);
  const topLink = topbar.querySelector(".top-link");
  if (topLink) topbar.insertBefore(wrap, topLink);
  else topbar.appendChild(wrap);
})();
