(() => {
  "use strict";

  const PROJECT = "https://github.com/SeekerThinker/word-writing-templates";
  const RAW = "https://raw.githubusercontent.com/SeekerThinker/word-writing-templates/main/templates";
  const PACKAGE = {
    windows: `${PROJECT}/releases/latest/download/Word-Writing-Templates-Windows.zip`,
    macos: `${PROJECT}/releases/latest/download/Word-Writing-Templates-macOS.zip`
  };

  const DATA = {
    book: {
      label: "Book / long-form",
      options: [
        { id: "book-cn-traditional", name: "Chinese traditional chapter numbering", file: "书籍-中文传统.dotx", folder: "books", preview: "book-cn-traditional.png", example: "第一章 → 第一节 → 一、 → （一）", desc: "A Chinese-style chapter numbering system for Chinese-language books, teaching materials, and traditional long-form writing.", recommended: true },
        { id: "book-chapter-decimal", name: "Chapter + decimal numbering", file: "书籍-章节数字.dotx", folder: "books", preview: "book-chapter-decimal.png", example: "Chapter 1 → 1.1 → 1.1.1 → 1.1.1.1", desc: "For technical books, tutorials, and research monographs." },
        { id: "book-pure-decimal", name: "Decimal long-form numbering", file: "书籍-纯数字.dotx", folder: "books", preview: "book-pure-decimal.png", example: "1 → 1.1 → 1.1.1 → 1.1.1.1", desc: "For clean modern long-form documents and ebooks." }
      ]
    },
    article: {
      label: "Article / everyday notes",
      options: [
        { id: "article-cn-academic", name: "Chinese academic numbering", file: "文章-中文论文.dotx", folder: "articles", preview: "article-cn-academic.png", example: "一、 → （一） → 1. → （1）", desc: "A Chinese academic numbering system for papers, reports, and formal Chinese-language articles.", recommended: true },
        { id: "article-decimal", name: "Decimal hierarchy", file: "文章-数字层级.dotx", folder: "articles", preview: "article-decimal.png", example: "1 → 1.1 → 1.1.1 → 1.1.1.1", desc: "For research, technical writing, and notes that benefit from explicit numbering." },
        { id: "article-cn-compact", name: "Compact Chinese numbering", file: "文章-中文简洁.dotx", folder: "articles", preview: "article-cn-compact.png", example: "一、 → 1. → （1） → ①", desc: "A compact Chinese numbering system for general articles, research notes, and everyday organization." }
      ]
    }
  };

  const state = { type: null, scheme: null, os: null };
  const el = {
    typeChoices: document.querySelector("#typeChoices"),
    schemeChoices: document.querySelector("#schemeChoices"),
    osChoices: document.querySelector("#osChoices"),
    stepScheme: document.querySelector("#stepScheme"),
    stepOs: document.querySelector("#stepOs"),
    osHint: document.querySelector("#osHint"),
    result: document.querySelector("#result"),
    resultTitle: document.querySelector("#resultTitle"),
    resultExample: document.querySelector("#resultExample"),
    resultDesc: document.querySelector("#resultDesc"),
    resultImage: document.querySelector("#resultImage"),
    templateDownload: document.querySelector("#templateDownload"),
    packageDownload: document.querySelector("#packageDownload"),
    resetBtn: document.querySelector("#resetBtn")
  };

  const allOptions = () => Object.values(DATA).flatMap((group) => group.options);
  const optionById = (id) => allOptions().find((item) => item.id === id);
  const typeForScheme = (id) => Object.entries(DATA).find(([, group]) => group.options.some((item) => item.id === id))?.[0] || null;

  function detectedOs() {
    const source = `${navigator.platform || ""} ${navigator.userAgent || ""}`;
    if (/Mac|iPhone|iPad/i.test(source)) return "macos";
    if (/Win/i.test(source)) return "windows";
    return null;
  }

  function setPressed(container, attr, value) {
    container.querySelectorAll(`[${attr}]`).forEach((button) => {
      const selected = button.getAttribute(attr) === value;
      button.classList.toggle("selected", selected);
      button.setAttribute("aria-pressed", selected ? "true" : "false");
    });
  }

  function lock(step, locked) {
    step.classList.toggle("locked", locked);
    step.setAttribute("aria-disabled", locked ? "true" : "false");
    step.toggleAttribute("inert", locked);
    step.querySelectorAll("button").forEach((button) => { button.disabled = locked; });
  }

  function renderSchemes() {
    const group = DATA[state.type];
    if (!group) return;
    el.schemeChoices.innerHTML = group.options.map((item) => `
      <button class="scheme" type="button" data-scheme="${item.id}" aria-pressed="false">
        ${item.recommended ? '<span class="recommend">Recommended</span>' : ""}
        <img src="../previews/${item.preview}" alt="${group.label}: ${item.name} numbering preview" loading="lazy" />
        <span class="scheme-copy"><strong>${item.name}</strong><code>${item.example}</code><small>${item.desc}</small></span>
      </button>`).join("");
    lock(el.stepScheme, false);
    setPressed(el.schemeChoices, "data-scheme", state.scheme);
  }

  function updateUrl() {
    const url = new URL(window.location.href);
    ["type", "scheme", "os"].forEach((key) => state[key] ? url.searchParams.set(key, state[key]) : url.searchParams.delete(key));
    url.searchParams.delete("variant");
    url.searchParams.delete("starter");
    history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
  }

  function renderResult() {
    if (!state.type || !state.scheme || !state.os) {
      el.result.hidden = true;
      updateUrl();
      return;
    }
    const item = optionById(state.scheme);
    const group = DATA[state.type];
    const platform = state.os === "windows" ? "Windows" : "macOS";
    const direct = `${RAW}/${state.os}/${item.folder}/${encodeURIComponent(item.file)}`;

    el.resultTitle.textContent = `${group.label} · ${item.name} · ${platform}`;
    el.resultExample.textContent = item.example;
    el.resultDesc.textContent = item.desc;
    el.resultImage.src = `../previews/${item.preview}`;
    el.templateDownload.href = direct;
    el.templateDownload.setAttribute("download", item.file);
    el.packageDownload.href = PACKAGE[state.os];
    el.packageDownload.textContent = `Download all ${platform} templates`;
    el.result.hidden = false;
    updateUrl();
  }

  function reset() {
    state.type = null;
    state.scheme = null;
    state.os = null;
    el.schemeChoices.innerHTML = '<div class="placeholder">Choose a structure first.</div>';
    lock(el.stepScheme, true);
    lock(el.stepOs, true);
    setPressed(el.typeChoices, "data-type", null);
    setPressed(el.osChoices, "data-os", null);
    el.result.hidden = true;
    updateUrl();
    document.querySelector("#chooser").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  el.typeChoices.addEventListener("click", (event) => {
    const button = event.target.closest("[data-type]");
    if (!button) return;
    state.type = button.dataset.type;
    state.scheme = null;
    state.os = null;
    setPressed(el.typeChoices, "data-type", state.type);
    setPressed(el.osChoices, "data-os", null);
    lock(el.stepOs, true);
    el.result.hidden = true;
    renderSchemes();
    updateUrl();
  });

  el.schemeChoices.addEventListener("click", (event) => {
    const button = event.target.closest("[data-scheme]");
    if (!button) return;
    state.scheme = button.dataset.scheme;
    setPressed(el.schemeChoices, "data-scheme", state.scheme);
    lock(el.stepOs, false);
    renderResult();
  });

  el.osChoices.addEventListener("click", (event) => {
    const button = event.target.closest("[data-os]");
    if (!button || el.stepOs.classList.contains("locked")) return;
    state.os = button.dataset.os;
    setPressed(el.osChoices, "data-os", state.os);
    renderResult();
    el.result.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  el.resetBtn.addEventListener("click", reset);

  const detected = detectedOs();
  if (detected) {
    const platform = detected === "macos" ? "macOS" : "Windows";
    el.osHint.textContent = `It looks like you are using ${platform}. If you use Word on another computer, choose that computer instead.`;
  }

  const params = new URLSearchParams(window.location.search);
  const scheme = params.get("scheme");
  const inferredType = scheme ? typeForScheme(scheme) : null;
  const type = params.get("type") || inferredType;
  const os = params.get("os");

  if (type && DATA[type]) state.type = type;
  if (state.type && scheme && DATA[state.type].options.some((item) => item.id === scheme)) state.scheme = scheme;
  if (os === "windows" || os === "macos") state.os = os;

  if (state.type) {
    setPressed(el.typeChoices, "data-type", state.type);
    renderSchemes();
  }
  if (state.scheme) {
    setPressed(el.schemeChoices, "data-scheme", state.scheme);
    lock(el.stepOs, false);
  }
  if (state.os) setPressed(el.osChoices, "data-os", state.os);
  renderResult();
})();
