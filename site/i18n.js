(() => {
  "use strict";

  const KEY = "word-writing-templates-language";
  const html = document.documentElement;
  const current = (html.lang || "zh-CN").toLowerCase().startsWith("en") ? "en" : "zh";
  const path = window.location.pathname;
  const page = /\/editor\.html$/.test(path) ? "editor" : /\/guide\.html$/.test(path) ? "guide" : "home";

  function withQueryAndHash(target) {
    return `${target}${window.location.search}${window.location.hash}`;
  }

  function targetFor(lang) {
    if (current === lang) return window.location.href;
    const file = page === "editor" ? "editor.html" : page === "guide" ? "guide.html" : "";
    if (current === "zh" && lang === "en") return withQueryAndHash(file ? `./en/${file}` : "./en/");
    if (current === "en" && lang === "zh") return withQueryAndHash(file ? `../${file}` : "../");
    return window.location.href;
  }

  function preferredLanguage() {
    try {
      const saved = localStorage.getItem(KEY);
      if (saved === "zh" || saved === "en") return saved;
    } catch (_) {}
    const primary = (navigator.languages && navigator.languages[0]) || navigator.language || "";
    return /^zh(?:-|$)/i.test(primary) ? "zh" : "en";
  }

  function remember(lang) {
    try { localStorage.setItem(KEY, lang); } catch (_) {}
  }

  if (current === "zh" && preferredLanguage() === "en") {
    window.location.replace(targetFor("en"));
    return;
  }

  const topbar = document.querySelector(".topbar, .editor-topbar");
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
    .editor-topbar .language-switch { margin-left: auto; }
    .editor-topbar .language-switch + .editor-top-actions { margin-left: 0; }
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
  const editorActions = topbar.querySelector(".editor-top-actions");
  if (topLink) topbar.insertBefore(wrap, topLink);
  else if (editorActions) topbar.insertBefore(wrap, editorActions);
  else topbar.appendChild(wrap);

  if (page === "home") {
    const actions = document.querySelector(".hero .hero-actions");
    if (actions && !actions.querySelector("[data-online-editor]")) {
      const online = document.createElement("a");
      online.className = "btn quiet";
      online.dataset.onlineEditor = "true";
      online.href = "./editor.html";
      online.textContent = current === "en" ? "Start online" : "在线开始";
      actions.appendChild(online);
    }
  }

  const footerLinks = document.querySelector("footer .footer-links");
  if (footerLinks && !footerLinks.querySelector("[data-editor-link]")) {
    const link = document.createElement("a");
    link.dataset.editorLink = "true";
    link.href = page === "home" ? "./editor.html" : current === "en" ? "./editor.html" : "./editor.html";
    link.textContent = current === "en" ? "Online editor" : "在线写作";
    footerLinks.insertBefore(link, footerLinks.firstChild);
  }

  if (page === "editor" && !document.querySelector("script[data-editor-copy]")) {
    const copy = document.createElement("script");
    copy.dataset.editorCopy = "true";
    copy.src = current === "en" ? "../editor-copy.js" : "./editor-copy.js";
    document.body.appendChild(copy);
  }
})();