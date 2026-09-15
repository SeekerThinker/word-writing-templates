(() => {
  "use strict";

  const isEn = (document.documentElement.lang || "").toLowerCase().startsWith("en");
  const W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main";
  const XML_NS = "http://www.w3.org/XML/1998/namespace";
  const DRAFT_DB = "word-writing-templates-editor";
  const DRAFT_STORE = "drafts";
  const DRAFT_KEY = "current";
  const VIEW_MODES = new Set(["continuous", "pages", "focus"]);

  const TEXT = isEn ? {
    untitled: "Untitled document",
    firstHeading: "First heading",
    firstBody: "Start writing here.\n\nUse the structure on the left to keep the whole document visible.",
    newHeading: "New heading",
    saved: "Saved locally",
    saving: "Saving…",
    localOnly: "Stored only in this browser",
    exportPreparing: "Preparing Word document…",
    exportDone: "Word document exported",
    exportError: "Could not export Word document",
    importError: "This backup file is not valid.",
    replaceConfirm: "Start a new document? The current draft will be replaced (you can export a JSON backup first).",
    deleteConfirm: "Delete this heading and everything nested under it?",
    mergeConfirm: "Merge this section into the previous sibling? Its heading will become bold text in the previous section.",
    noPrevious: "There is no previous sibling to merge into.",
    templateFetchError: "The Word template could not be loaded. Check your connection and try again.",
    editorEmpty: "Select a heading on the left.",
    docLangHintZh: "Chinese document: keep the template's platform-specific Chinese fonts.",
    docLangHintEn: "English document: export uses Times New Roman for body text and Arial for headings. “Chapter + decimals” becomes Chapter 1 → 1.1 → …",
    headingsOnlyHint: "Heading numbering is suppressed in the exported Word file; heading levels and Navigation Pane structure remain.",
    numberedHint: "The selected Word numbering preset is retained in the exported document.",
    backupName: "structured-writing-backup",
    wordName: "structured-writing",
    unsupportedZip: "The export library did not load. Reload the page and try again.",
    continuousHint: "Full document: edit every section in one continuous scroll. Selecting an outline heading jumps to the same place in the document.",
    focusHint: "Focus mode: show only the selected section and its nested subsections.",
    pagesHint: "Page preview: browse the whole document on paper-like pages. This view is read-only and pagination is approximate.",
    textPlaceholder: "Write this section…"
  } : {
    untitled: "未命名文档",
    firstHeading: "第一个标题",
    firstBody: "从这里开始记录。\n\n左边保留整体结构，右边浏览和编辑整篇文档。",
    newHeading: "新标题",
    saved: "已保存到本机",
    saving: "正在保存…",
    localOnly: "内容只保存在这个浏览器中",
    exportPreparing: "正在生成 Word 文档…",
    exportDone: "Word 文档已导出",
    exportError: "无法导出 Word 文档",
    importError: "这个备份文件无法识别。",
    replaceConfirm: "新建文档会替换当前草稿。要继续吗？（可以先导出 JSON 备份）",
    deleteConfirm: "删除这个标题以及它下面的全部子标题和正文？",
    mergeConfirm: "把这一节合并到前一个同级标题吗？当前标题会作为加粗文字并入前一节正文。",
    noPrevious: "前面没有可以合并的同级标题。",
    templateFetchError: "无法载入 Word 模板。请检查网络后重试。",
    editorEmpty: "请先在左边选择一个标题。",
    docLangHintZh: "中文文档：导出时保留模板针对 Windows / macOS 设置的中文字体。",
    docLangHintEn: "英文文档：导出时正文改用 Times New Roman，标题改用 Arial；“章节数字”会导出为 Chapter 1 → 1.1 → …。",
    headingsOnlyHint: "导出的 Word 会关闭标题编号，但仍保留真实标题层级和导航窗格结构。",
    numberedHint: "导出的 Word 会保留所选编号方案。",
    backupName: "结构化写作备份",
    wordName: "结构化写作",
    unsupportedZip: "导出组件没有成功载入。请刷新页面后重试。",
    continuousHint: "全文模式：整篇文档连续显示并可直接编辑；点击左侧标题会定位到正文中的同一位置。",
    focusHint: "专注模式：只显示当前标题以及它下面的子标题和正文。",
    pagesHint: "页面预览：以纸张形式浏览全文；此视图只读，分页为近似预览。",
    textPlaceholder: "在这一节继续写…"
  };

  const PRESETS = {
    "book-cn-traditional": { folder: "books", file: "书籍-中文传统.dotx", zh: "中文传统章节编号", en: "Chinese traditional chapter numbering", exampleZh: "第一章 → 第一节 → 一、 → （一）", exampleEn: "Chinese numerals: 第一章 → 第一节 → 一、 → （一）" },
    "book-chapter-decimal": { folder: "books", file: "书籍-章节数字.dotx", zh: "章节数字", en: "Chapter + decimal numbering", exampleZh: "第1章 → 1.1 → 1.1.1 → 1.1.1.1", exampleEn: "Chapter 1 → 1.1 → 1.1.1 → 1.1.1.1" },
    "book-pure-decimal": { folder: "books", file: "书籍-纯数字.dotx", zh: "长篇纯数字", en: "Decimal long-form numbering", exampleZh: "1 → 1.1 → 1.1.1 → 1.1.1.1", exampleEn: "1 → 1.1 → 1.1.1 → 1.1.1.1" },
    "article-cn-academic": { folder: "articles", file: "文章-中文论文.dotx", zh: "中文论文编号", en: "Chinese academic numbering", exampleZh: "一、 → （一） → 1. → （1）", exampleEn: "Chinese academic: 一、 → （一） → 1. → （1）" },
    "article-decimal": { folder: "articles", file: "文章-数字层级.dotx", zh: "数字层级", en: "Decimal hierarchy", exampleZh: "1 → 1.1 → 1.1.1 → 1.1.1.1", exampleEn: "1 → 1.1 → 1.1.1 → 1.1.1.1" },
    "article-cn-compact": { folder: "articles", file: "文章-中文简洁.dotx", zh: "中文简洁编号", en: "Compact Chinese numbering", exampleZh: "一、 → 1. → （1） → ①", exampleEn: "Compact Chinese: 一、 → 1. → （1） → ①" }
  };

  const $ = (sel) => document.querySelector(sel);
  const el = {
    title: $("#docTitle"), outline: $("#outlineList"), addRoot: $("#addRoot"), canvas: $("#documentCanvas"), selectedLevel: $("#selectedLevel"),
    addSibling: $("#addSibling"), addChild: $("#addChild"), promote: $("#promote"), demote: $("#demote"), moveUp: $("#moveUp"), moveDown: $("#moveDown"), split: $("#splitSection"), merge: $("#mergePrevious"), remove: $("#deleteSection"),
    bold: $("#fmtBold"), italic: $("#fmtItalic"), quote: $("#fmtQuote"), bullet: $("#fmtBullet"), number: $("#fmtNumber"), clear: $("#fmtClear"),
    docLanguage: $("#docLanguage"), platform: $("#platform"), preset: $("#preset"), headingsOnly: $("#headingsOnly"), formatHint: $("#formatHint"),
    saveStatus: $("#saveStatus"), newDoc: $("#newDoc"), exportWord: $("#exportWord"), exportJson: $("#exportJson"), importJson: $("#importJson"), importFile: $("#importFile"), privacy: $("#privacyNote"),
    viewNote: $("#viewNote"), viewContinuous: $("#viewContinuous"), viewPages: $("#viewPages"), viewFocus: $("#viewFocus")
  };

  let state = defaultState();
  let saveTimer = null;
  let dbPromise = null;
  let draggingId = null;
  let scrollSyncQueued = false;
  let suppressScrollSyncUntil = 0;

  function uid() { return crypto && crypto.randomUUID ? crypto.randomUUID() : `s-${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`; }
  function detectedPlatform() { const src = `${navigator.platform || ""} ${navigator.userAgent || ""}`; return /Mac|iPhone|iPad/i.test(src) ? "macos" : "windows"; }
  function defaultState() {
    const id = uid();
    return { version: 2, title: TEXT.untitled, docLanguage: isEn ? "en" : "zh", platform: detectedPlatform(), preset: "article-decimal", headingsOnly: false, viewMode: "continuous", selectedId: id, nodes: [{ id, level: 1, title: TEXT.firstHeading, body: TEXT.firstBody }], updatedAt: Date.now() };
  }
  function normalizeState(input) {
    if (!input || typeof input !== "object" || !Array.isArray(input.nodes)) throw new Error("bad state");
    const nodes = input.nodes.filter(Boolean).map((n) => ({ id: typeof n.id === "string" && n.id ? n.id : uid(), level: Math.max(1, Math.min(4, Number(n.level) || 1)), title: String(n.title ?? ""), body: String(n.body ?? "") }));
    if (!nodes.length) nodes.push({ id: uid(), level: 1, title: TEXT.firstHeading, body: "" });
    return { version: 2, title: String(input.title || TEXT.untitled), docLanguage: input.docLanguage === "en" ? "en" : "zh", platform: input.platform === "macos" ? "macos" : "windows", preset: PRESETS[input.preset] ? input.preset : "article-decimal", headingsOnly: Boolean(input.headingsOnly), viewMode: VIEW_MODES.has(input.viewMode) ? input.viewMode : "continuous", selectedId: nodes.some((n) => n.id === input.selectedId) ? input.selectedId : nodes[0].id, nodes, updatedAt: Number(input.updatedAt) || Date.now() };
  }

  function openDb() {
    if (!window.indexedDB) return Promise.resolve(null);
    if (dbPromise) return dbPromise;
    dbPromise = new Promise((resolve) => {
      const req = indexedDB.open(DRAFT_DB, 1);
      req.onupgradeneeded = () => { const db = req.result; if (!db.objectStoreNames.contains(DRAFT_STORE)) db.createObjectStore(DRAFT_STORE); };
      req.onsuccess = () => resolve(req.result); req.onerror = () => resolve(null);
    });
    return dbPromise;
  }
  async function loadDraft() {
    const db = await openDb();
    if (!db) { try { const raw = localStorage.getItem(DRAFT_DB); return raw ? JSON.parse(raw) : null; } catch (_) { return null; } }
    return new Promise((resolve) => { const tx = db.transaction(DRAFT_STORE, "readonly"); const req = tx.objectStore(DRAFT_STORE).get(DRAFT_KEY); req.onsuccess = () => resolve(req.result || null); req.onerror = () => resolve(null); });
  }
  async function saveDraftNow() {
    state.updatedAt = Date.now(); setStatus(TEXT.saving); const snapshot = JSON.parse(JSON.stringify(state)); const db = await openDb();
    if (!db) { try { localStorage.setItem(DRAFT_DB, JSON.stringify(snapshot)); } catch (_) {} setStatus(TEXT.saved); return; }
    await new Promise((resolve) => { const tx = db.transaction(DRAFT_STORE, "readwrite"); tx.objectStore(DRAFT_STORE).put(snapshot, DRAFT_KEY); tx.oncomplete = resolve; tx.onerror = resolve; });
    setStatus(TEXT.saved);
  }
  function scheduleSave() { clearTimeout(saveTimer); setStatus(TEXT.saving); saveTimer = setTimeout(saveDraftNow, 450); }
  function setStatus(message) { if (el.saveStatus) el.saveStatus.textContent = message; }
  function selectedIndex() { return state.nodes.findIndex((n) => n.id === state.selectedId); }
  function selectedNode() { return state.nodes[selectedIndex()] || null; }
  function subtreeEnd(index, nodes = state.nodes) { if (index < 0 || index >= nodes.length) return index; const level = nodes[index].level; let i = index + 1; while (i < nodes.length && nodes[i].level > level) i++; return i; }
  function previousSiblingIndex(index) { if (index <= 0) return -1; const level = state.nodes[index].level; for (let i = index - 1; i >= 0; i--) { if (state.nodes[i].level < level) return -1; if (state.nodes[i].level === level) return i; } return -1; }
  function nextSiblingIndex(index) { const end = subtreeEnd(index); return end < state.nodes.length && state.nodes[end].level === state.nodes[index].level ? end : -1; }

  function cn(n) { const d = ["零","一","二","三","四","五","六","七","八","九"]; if (n <= 10) return n === 10 ? "十" : d[n] || String(n); if (n < 20) return `十${d[n % 10]}`; if (n < 100) return `${d[Math.floor(n / 10)]}十${n % 10 ? d[n % 10] : ""}`; return String(n); }
  function circled(n) { const chars = ["","①","②","③","④","⑤","⑥","⑦","⑧","⑨","⑩","⑪","⑫","⑬","⑭","⑮","⑯","⑰","⑱","⑲","⑳"]; return chars[n] || String(n); }
  function numberingLabels() {
    const counts = [0,0,0,0];
    return state.nodes.map((node) => {
      const l = node.level - 1; counts[l] += 1; for (let i = l + 1; i < 4; i++) counts[i] = 0; if (state.headingsOnly) return ""; const c = counts;
      switch (state.preset) {
        case "book-cn-traditional": return node.level === 1 ? `第${cn(c[0])}章` : node.level === 2 ? `第${cn(c[1])}节` : node.level === 3 ? `${cn(c[2])}、` : `（${cn(c[3])}）`;
        case "book-chapter-decimal": if (node.level === 1) return state.docLanguage === "en" ? `Chapter ${c[0]}` : `第${c[0]}章`; return c.slice(0,node.level).filter(Boolean).join(".");
        case "book-pure-decimal": case "article-decimal": return c.slice(0,node.level).filter(Boolean).join(".");
        case "article-cn-academic": return node.level === 1 ? `${cn(c[0])}、` : node.level === 2 ? `（${cn(c[1])}）` : node.level === 3 ? `${c[2]}.` : `（${c[3]}）`;
        case "article-cn-compact": return node.level === 1 ? `${cn(c[0])}、` : node.level === 2 ? `${c[1]}.` : node.level === 3 ? `（${c[2]}）` : circled(c[3]);
        default: return "";
      }
    });
  }

  function renderPresetOptions() {
    const current = state.preset; el.preset.textContent = "";
    for (const [id,p] of Object.entries(PRESETS)) { const option = document.createElement("option"); option.value = id; option.textContent = `${isEn ? p.en : p.zh} — ${state.docLanguage === "en" ? p.exampleEn : p.exampleZh}`; option.selected = id === current; el.preset.appendChild(option); }
  }
  function renderOutline() {
    const labels = numberingLabels(); el.outline.textContent = "";
    state.nodes.forEach((node,index) => {
      const row = document.createElement("button"); row.type = "button"; row.className = "outline-item"; row.draggable = true; row.dataset.id = node.id; row.style.setProperty("--level", node.level - 1); row.setAttribute("aria-pressed", node.id === state.selectedId ? "true" : "false");
      const grip = document.createElement("span"); grip.className = "outline-grip"; grip.textContent = "⋮⋮"; grip.setAttribute("aria-hidden","true");
      const badge = document.createElement("span"); badge.className = "outline-level"; badge.textContent = `H${node.level}`;
      const copy = document.createElement("span"); copy.className = "outline-copy"; const num = document.createElement("small"); num.textContent = labels[index]; const title = document.createElement("strong"); title.textContent = node.title || TEXT.newHeading; copy.append(num,title); row.append(grip,badge,copy);
      row.addEventListener("click", () => selectNode(node.id, true));
      row.addEventListener("dragstart", (event) => { draggingId = node.id; row.classList.add("dragging"); if (event.dataTransfer) { event.dataTransfer.effectAllowed = "move"; event.dataTransfer.setData("text/plain",node.id); } });
      row.addEventListener("dragend", () => { draggingId = null; row.classList.remove("dragging"); document.querySelectorAll(".drop-before,.drop-after").forEach((x) => x.classList.remove("drop-before","drop-after")); });
      row.addEventListener("dragover", (event) => { if (!draggingId || draggingId === node.id) return; event.preventDefault(); const r = row.getBoundingClientRect(); const after = event.clientY > r.top + r.height/2; row.classList.toggle("drop-after",after); row.classList.toggle("drop-before",!after); });
      row.addEventListener("dragleave", () => row.classList.remove("drop-before","drop-after"));
      row.addEventListener("drop", (event) => { event.preventDefault(); const r = row.getBoundingClientRect(); moveSubtree(draggingId,node.id,event.clientY > r.top + r.height/2); });
      el.outline.appendChild(row);
    });
  }
  function updateOutlineSelection() { el.outline.querySelectorAll(".outline-item").forEach((row) => row.setAttribute("aria-pressed", row.dataset.id === state.selectedId ? "true" : "false")); }
  function updateOutlineNode(id) { const row = el.outline.querySelector(`.outline-item[data-id="${CSS.escape(id)}"]`); const node = state.nodes.find((n) => n.id === id); if (row && node) row.querySelector("strong").textContent = node.title || TEXT.newHeading; }
  function autoSize(ta) { if (!ta) return; ta.style.height = "auto"; ta.style.height = `${Math.max(96, ta.scrollHeight + 2)}px`; }
  function documentNodesForView() { if (state.viewMode !== "focus") return state.nodes; const idx = selectedIndex(); return idx < 0 ? [] : state.nodes.slice(idx, subtreeEnd(idx)); }

  function makeEditableSection(node, index, labels) {
    const section = document.createElement("article"); section.className = "document-section"; section.dataset.id = node.id; section.dataset.level = String(node.level); section.classList.toggle("selected", node.id === state.selectedId);
    const headingRow = document.createElement("div"); headingRow.className = `doc-heading-row level-${node.level}`;
    const num = document.createElement("span"); num.className = "doc-heading-number"; num.textContent = labels[index]; num.hidden = !labels[index];
    const heading = document.createElement("input"); heading.type = "text"; heading.className = "doc-heading-input"; heading.value = node.title; heading.placeholder = TEXT.newHeading; heading.dataset.id = node.id; heading.setAttribute("aria-label", `${isEn ? "Heading" : "标题"} ${node.level}`);
    heading.addEventListener("focus", () => selectNode(node.id, false));
    heading.addEventListener("input", () => { node.title = heading.value; updateOutlineNode(node.id); scheduleSave(); });
    headingRow.append(num, heading);
    const body = document.createElement("textarea"); body.className = "doc-body"; body.dataset.id = node.id; body.value = node.body; body.spellcheck = true; body.placeholder = TEXT.textPlaceholder; body.setAttribute("aria-label", isEn ? `Body for ${node.title || TEXT.newHeading}` : `${node.title || TEXT.newHeading}的正文`);
    body.addEventListener("focus", () => selectNode(node.id, false));
    body.addEventListener("input", () => { node.body = body.value; autoSize(body); scheduleSave(); });
    section.append(headingRow, body); return section;
  }
  function inlineTitleInput() {
    const input = document.createElement("input"); input.type = "text"; input.className = "inline-doc-title"; input.value = state.title; input.setAttribute("aria-label", isEn ? "Document title in document view" : "全文视图中的文档标题");
    input.addEventListener("input", () => { state.title = input.value; el.title.value = input.value; scheduleSave(); }); return input;
  }
  function appendPreviewInline(parent, text) {
    const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g; let cursor = 0;
    for (const match of String(text).matchAll(re)) { if (match.index > cursor) parent.append(document.createTextNode(text.slice(cursor, match.index))); const token = match[0]; const mark = document.createElement(token.startsWith("**") ? "strong" : "em"); mark.textContent = token.startsWith("**") ? token.slice(2,-2) : token.slice(1,-1); parent.append(mark); cursor = match.index + token.length; }
    if (cursor < text.length) parent.append(document.createTextNode(text.slice(cursor)));
  }
  function previewBlocks(labels) {
    const blocks = [];
    if (state.title.trim()) { const title = document.createElement("div"); title.className = "preview-doc-title"; title.textContent = state.title.trim(); blocks.push(title); }
    state.nodes.forEach((node,index) => {
      const heading = document.createElement("div"); heading.className = `preview-heading level-${node.level}`; heading.dataset.id = node.id; const prefix = labels[index] ? `${labels[index]} ` : ""; heading.textContent = `${prefix}${node.title || TEXT.newHeading}`; heading.addEventListener("click", () => selectNode(node.id, false)); blocks.push(heading);
      for (const raw of String(node.body || "").replace(/\r\n?/g,"\n").split("\n")) { const p = document.createElement("p"); p.className = "preview-paragraph"; p.dataset.id = node.id; let text = raw; if (/^>\s?/.test(text)) { p.classList.add("quote"); text = text.replace(/^>\s?/,""); } else if (/^\s*[-*]\s+/.test(text)) { p.classList.add("bullet"); text = text.replace(/^\s*[-*]\s+/,""); } else if (/^\s*\d+\.\s+/.test(text)) { p.classList.add("numbered"); text = text.replace(/^\s*\d+\.\s+/,""); } if (text) appendPreviewInline(p,text); else p.innerHTML = "&nbsp;"; blocks.push(p); }
    });
    return blocks;
  }
  function newPreviewPage(number) { const page = document.createElement("section"); page.className = "preview-page"; const content = document.createElement("div"); content.className = "preview-page-content"; const footer = document.createElement("div"); footer.className = "preview-page-number"; footer.textContent = String(number); page.append(content,footer); el.canvas.appendChild(page); return content; }
  function renderPagePreview(labels) {
    el.canvas.className = "document-canvas page-preview"; let pageNumber = 1; let content = newPreviewPage(pageNumber);
    for (const block of previewBlocks(labels)) { content.appendChild(block); if (content.scrollHeight > content.clientHeight && content.children.length > 1) { content.removeChild(block); content = newPreviewPage(++pageNumber); content.appendChild(block); } }
  }
  function renderDocument() {
    const labels = numberingLabels(); el.canvas.textContent = "";
    if (state.viewMode === "pages") { renderPagePreview(labels); updateViewUI(); updateActionState(); return; }
    el.canvas.className = `document-canvas editable-view ${state.viewMode === "focus" ? "focus-view" : "continuous-view"}`;
    const flow = document.createElement("div"); flow.className = "document-flow"; flow.appendChild(inlineTitleInput());
    for (const node of documentNodesForView()) { const index = state.nodes.findIndex((item) => item.id === node.id); flow.appendChild(makeEditableSection(node,index,labels)); }
    el.canvas.appendChild(flow); requestAnimationFrame(() => el.canvas.querySelectorAll(".doc-body").forEach(autoSize)); updateViewUI(); updateActionState();
  }
  function updateViewUI() {
    const buttons = { continuous: el.viewContinuous, pages: el.viewPages, focus: el.viewFocus };
    for (const [mode,button] of Object.entries(buttons)) { button.classList.toggle("active", state.viewMode === mode); button.setAttribute("aria-pressed", state.viewMode === mode ? "true" : "false"); }
    el.viewNote.textContent = state.viewMode === "pages" ? TEXT.pagesHint : state.viewMode === "focus" ? TEXT.focusHint : TEXT.continuousHint;
  }
  function updateActionState() {
    const node = selectedNode(); const controls = [el.addSibling,el.addChild,el.promote,el.demote,el.moveUp,el.moveDown,el.split,el.merge,el.remove].filter(Boolean);
    if (!node) { controls.forEach((c) => c.disabled = true); el.selectedLevel.textContent = TEXT.editorEmpty; return; }
    controls.forEach((c) => c.disabled = false); el.selectedLevel.textContent = `Heading ${node.level} · H${node.level}`;
    const idx = selectedIndex(); el.promote.disabled = node.level <= 1; el.demote.disabled = node.level >= 4 || previousSiblingIndex(idx) < 0 || state.nodes.slice(idx,subtreeEnd(idx)).some((n) => n.level >= 4); el.moveUp.disabled = previousSiblingIndex(idx) < 0; el.moveDown.disabled = nextSiblingIndex(idx) < 0; el.addChild.disabled = node.level >= 4; el.merge.disabled = previousSiblingIndex(idx) < 0; el.split.disabled = state.viewMode === "pages";
    for (const c of [el.bold,el.italic,el.quote,el.bullet,el.number,el.clear]) c.disabled = state.viewMode === "pages";
    el.canvas.querySelectorAll(".document-section").forEach((section) => section.classList.toggle("selected", section.dataset.id === state.selectedId));
  }
  function renderSettings() { el.title.value = state.title; el.docLanguage.value = state.docLanguage; el.platform.value = state.platform; renderPresetOptions(); el.headingsOnly.checked = state.headingsOnly; updateFormatHint(); }
  function renderAll() { renderSettings(); renderOutline(); renderDocument(); }
  function updateFormatHint() { el.formatHint.textContent = `${state.docLanguage === "en" ? TEXT.docLangHintEn : TEXT.docLangHintZh} ${state.headingsOnly ? TEXT.headingsOnlyHint : TEXT.numberedHint}`; }

  function scrollToSelected() {
    const selector = state.viewMode === "pages" ? `.preview-heading[data-id="${CSS.escape(state.selectedId)}"]` : `.document-section[data-id="${CSS.escape(state.selectedId)}"]`; const target = el.canvas.querySelector(selector);
    if (target) { suppressScrollSyncUntil = Date.now() + 900; target.scrollIntoView({ behavior: "smooth", block: "start" }); }
  }
  function selectNode(id, shouldScroll = false) {
    if (!state.nodes.some((n) => n.id === id)) return; const changed = state.selectedId !== id; state.selectedId = id; updateOutlineSelection(); if (state.viewMode === "focus" && changed) renderDocument(); else updateActionState(); if (shouldScroll) requestAnimationFrame(scrollToSelected); scheduleSave();
  }
  function setView(mode) { if (!VIEW_MODES.has(mode) || state.viewMode === mode) return; state.viewMode = mode; renderDocument(); scheduleSave(); requestAnimationFrame(scrollToSelected); }
  function syncSelectionFromScroll() {
    scrollSyncQueued = false; if (state.viewMode !== "continuous" || Date.now() < suppressScrollSyncUntil) return; const sections = [...el.canvas.querySelectorAll(".document-section")]; if (!sections.length) return; const anchor = Math.min(window.innerHeight * .32, 260); let best = sections[0]; for (const section of sections) { const rect = section.getBoundingClientRect(); if (rect.top <= anchor) best = section; else break; } if (best.dataset.id && best.dataset.id !== state.selectedId) { state.selectedId = best.dataset.id; updateOutlineSelection(); updateActionState(); }
  }
  function onScroll() { if (!scrollSyncQueued) { scrollSyncQueued = true; requestAnimationFrame(syncSelectionFromScroll); } }

  function addNode(kind) {
    const idx = selectedIndex(); if (idx < 0) return; const current = state.nodes[idx], end = subtreeEnd(idx); const node = { id: uid(), level: kind === "child" ? Math.min(4,current.level+1) : current.level, title: TEXT.newHeading, body: "" }; state.nodes.splice(end,0,node); state.selectedId = node.id; renderAll(); scheduleSave(); requestAnimationFrame(() => { scrollToSelected(); const input = el.canvas.querySelector(`.doc-heading-input[data-id="${CSS.escape(node.id)}"]`); if (input) input.select(); });
  }
  function addRoot() { const node = { id: uid(), level: 1, title: TEXT.newHeading, body: "" }; state.nodes.push(node); state.selectedId = node.id; renderAll(); scheduleSave(); requestAnimationFrame(() => { scrollToSelected(); const input = el.canvas.querySelector(`.doc-heading-input[data-id="${CSS.escape(node.id)}"]`); if (input) input.select(); }); }
  function promote() { const idx = selectedIndex(); if (idx < 0 || state.nodes[idx].level <= 1) return; const end = subtreeEnd(idx); for (let i=idx;i<end;i++) state.nodes[i].level -= 1; renderAll(); scheduleSave(); requestAnimationFrame(scrollToSelected); }
  function demote() { const idx = selectedIndex(); if (idx < 0 || state.nodes[idx].level >= 4 || previousSiblingIndex(idx) < 0) return; const end = subtreeEnd(idx); if (state.nodes.slice(idx,end).some((n) => n.level >= 4)) return; for (let i=idx;i<end;i++) state.nodes[i].level += 1; renderAll(); scheduleSave(); requestAnimationFrame(scrollToSelected); }
  function moveUp() { const idx = selectedIndex(), prev = previousSiblingIndex(idx); if (prev < 0) return; const end = subtreeEnd(idx), block = state.nodes.splice(idx,end-idx); state.nodes.splice(prev,0,...block); renderAll(); scheduleSave(); requestAnimationFrame(scrollToSelected); }
  function moveDown() { const idx = selectedIndex(), next = nextSiblingIndex(idx); if (next < 0) return; const end = subtreeEnd(idx), targetEnd = subtreeEnd(next), block = state.nodes.slice(idx,end), target = state.nodes.slice(next,targetEnd); state.nodes.splice(idx,targetEnd-idx,...target,...block); renderAll(); scheduleSave(); requestAnimationFrame(scrollToSelected); }
  function moveSubtree(dragId,targetId,after) {
    if (!dragId || dragId === targetId) return; const sourceIndex = state.nodes.findIndex((n) => n.id === dragId), targetIndex = state.nodes.findIndex((n) => n.id === targetId); if (sourceIndex < 0 || targetIndex < 0) return; const sourceEnd = subtreeEnd(sourceIndex); if (targetIndex >= sourceIndex && targetIndex < sourceEnd) return; const block = state.nodes.slice(sourceIndex,sourceEnd); state.nodes.splice(sourceIndex,block.length); const newTarget = state.nodes.findIndex((n) => n.id === targetId), insertAt = after ? subtreeEnd(newTarget) : newTarget; state.nodes.splice(insertAt,0,...block); state.selectedId = dragId; renderAll(); scheduleSave(); requestAnimationFrame(scrollToSelected);
  }
  function currentBodyInput() { return el.canvas.querySelector(`.doc-body[data-id="${CSS.escape(state.selectedId)}"]`); }
  function splitSection() { const idx = selectedIndex(); if (idx < 0 || state.viewMode === "pages") return; const ta = currentBodyInput(), cursor = ta ? (ta.selectionStart ?? state.nodes[idx].body.length) : state.nodes[idx].body.length, before = state.nodes[idx].body.slice(0,cursor).replace(/\s+$/,""); const after = state.nodes[idx].body.slice(cursor).replace(/^\s+/,""); state.nodes[idx].body = before; const node = { id: uid(), level: state.nodes[idx].level, title: TEXT.newHeading, body: after }; state.nodes.splice(subtreeEnd(idx),0,node); state.selectedId = node.id; renderAll(); scheduleSave(); requestAnimationFrame(() => { scrollToSelected(); const input = el.canvas.querySelector(`.doc-heading-input[data-id="${CSS.escape(node.id)}"]`); if (input) input.select(); }); }
  function mergePrevious() { const idx = selectedIndex(), prev = previousSiblingIndex(idx); if (prev < 0) { alert(TEXT.noPrevious); return; } if (!confirm(TEXT.mergeConfirm)) return; const current = state.nodes[idx], previous = state.nodes[prev]; previous.body = [previous.body, `**${current.title || TEXT.newHeading}**`, current.body].filter(Boolean).join("\n\n"); state.nodes.splice(idx,1); state.selectedId = previous.id; renderAll(); scheduleSave(); requestAnimationFrame(scrollToSelected); }
  function deleteSection() { const idx = selectedIndex(); if (idx < 0 || !confirm(TEXT.deleteConfirm)) return; state.nodes.splice(idx,subtreeEnd(idx)-idx); if (!state.nodes.length) { const node = { id: uid(), level: 1, title: TEXT.newHeading, body: "" }; state.nodes.push(node); state.selectedId = node.id; } else state.selectedId = state.nodes[Math.min(idx,state.nodes.length-1)].id; renderAll(); scheduleSave(); requestAnimationFrame(scrollToSelected); }
  function applyInline(marker) { const ta = currentBodyInput(); if (!ta) return; const start=ta.selectionStart,end=ta.selectionEnd,value=ta.value,selected=value.slice(start,end)||(isEn?"text":"文字"); ta.setRangeText(`${marker}${selected}${marker}`,start,end,"select"); ta.dispatchEvent(new Event("input",{bubbles:true})); ta.focus(); }
  function applyLinePrefix(kind) { const ta = currentBodyInput(); if (!ta) return; const value=ta.value,start=value.lastIndexOf("\n",Math.max(0,ta.selectionStart-1))+1,rawEnd=value.indexOf("\n",ta.selectionEnd),end=rawEnd===-1?value.length:rawEnd,clean=value.slice(start,end).split("\n").map((line)=>line.replace(/^\s*(?:>\s+|[-*]\s+|\d+\.\s+)/,"")); let out; if(kind==="quote") out=clean.map((l)=>`> ${l}`).join("\n"); else if(kind==="bullet") out=clean.map((l)=>`- ${l}`).join("\n"); else if(kind==="number") out=clean.map((l,i)=>`${i+1}. ${l}`).join("\n"); else out=clean.join("\n"); ta.setRangeText(out,start,end,"select"); ta.dispatchEvent(new Event("input",{bubbles:true})); ta.focus(); }

  function newDocument() { if (!confirm(TEXT.replaceConfirm)) return; state = defaultState(); renderAll(); saveDraftNow(); }
  function sanitizeFileName(name,fallback) { const cleaned=String(name||"").replace(/[\\/:*?"<>|\u0000-\u001F]/g," ").replace(/\s+/g," ").trim().slice(0,100); return cleaned||fallback; }
  function downloadBlob(blob,name) { const url=URL.createObjectURL(blob),a=document.createElement("a"); a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000); }
  function exportBackup() { downloadBlob(new Blob([JSON.stringify(state,null,2)],{type:"application/json;charset=utf-8"}),`${sanitizeFileName(state.title,TEXT.backupName)}.json`); }
  async function importBackup(file) { try { state = normalizeState(JSON.parse(await file.text())); renderAll(); await saveDraftNow(); } catch (_) { alert(TEXT.importError); } }

  function templateUrl() { const p=PRESETS[state.preset],prefix=isEn?"../templates":"./templates"; return `${prefix}/${state.platform}/${p.folder}/${encodeURIComponent(p.file)}`; }
  function xmlDoc(text) { const doc=new DOMParser().parseFromString(text,"application/xml"); if(doc.getElementsByTagName("parsererror").length) throw new Error("Invalid XML"); return doc; }
  function wEl(doc,local) { return doc.createElementNS(W,`w:${local}`); }
  function addPStyle(doc,p,styleId) { const pPr=wEl(doc,"pPr"),pStyle=wEl(doc,"pStyle");pStyle.setAttributeNS(W,"w:val",styleId);pPr.appendChild(pStyle);p.appendChild(pPr);return pPr; }
  function addRun(doc,p,text,format={}) { const r=wEl(doc,"r"); if(format.bold||format.italic){const rPr=wEl(doc,"rPr");if(format.bold)rPr.appendChild(wEl(doc,"b"));if(format.italic)rPr.appendChild(wEl(doc,"i"));r.appendChild(rPr);} const t=wEl(doc,"t");if(/^\s|\s$/.test(text))t.setAttributeNS(XML_NS,"xml:space","preserve");t.textContent=text;r.appendChild(t);p.appendChild(r); }
  function addInlineRuns(doc,p,text) { const re=/(\*\*[^*]+\*\*|\*[^*]+\*)/g;let cursor=0;for(const match of text.matchAll(re)){if(match.index>cursor)addRun(doc,p,text.slice(cursor,match.index));const token=match[0];token.startsWith("**")?addRun(doc,p,token.slice(2,-2),{bold:true}):addRun(doc,p,token.slice(1,-1),{italic:true});cursor=match.index+token.length;}if(cursor<text.length)addRun(doc,p,text.slice(cursor));if(!text.length)addRun(doc,p,""); }
  function addListNumPr(doc,pPr,numId) { const numPr=wEl(doc,"numPr"),ilvl=wEl(doc,"ilvl"),id=wEl(doc,"numId");ilvl.setAttributeNS(W,"w:val","0");id.setAttributeNS(W,"w:val",String(numId));numPr.append(ilvl,id);pPr.appendChild(numPr); }
  function makeParagraph(doc,text,style="BodyText",listNumId=null) { const p=wEl(doc,"p"),pPr=addPStyle(doc,p,style);if(listNumId!==null)addListNumPr(doc,pPr,listNumId);addInlineRuns(doc,p,text);return p; }
  function bodyParagraphs(doc,body) { const out=[];for(const raw of String(body||"").replace(/\r\n?/g,"\n").split("\n")){if(/^>\s?/.test(raw))out.push(makeParagraph(doc,raw.replace(/^>\s?/,""),"AC"));else if(/^\s*[-*]\s+/.test(raw))out.push(makeParagraph(doc,raw.replace(/^\s*[-*]\s+/,""),"BodyText",98));else if(/^\s*\d+\.\s+/.test(raw))out.push(makeParagraph(doc,raw.replace(/^\s*\d+\.\s+/,""),"BodyText",99));else out.push(makeParagraph(doc,raw,"BodyText"));}return out; }
  function removeHeadingNumbering(stylesXml) { const doc=xmlDoc(stylesXml);for(let level=1;level<=4;level++){const style=Array.from(doc.getElementsByTagNameNS(W,"style")).find((s)=>s.getAttributeNS(W,"styleId")===`Heading${level}`);if(!style)continue;const pPr=Array.from(style.childNodes).find((n)=>n.namespaceURI===W&&n.localName==="pPr");if(pPr)Array.from(pPr.childNodes).filter((n)=>n.namespaceURI===W&&n.localName==="numPr").forEach((n)=>pPr.removeChild(n));}return new XMLSerializer().serializeToString(doc); }
  function patchEnglishFonts(stylesXml) { if(state.docLanguage!=="en")return stylesXml;const doc=xmlDoc(stylesXml),fonts={Normal:"Times New Roman",BodyText:"Times New Roman",AC:"Times New Roman",FootnoteText:"Times New Roman",Title:"Arial",Heading1:"Arial",Heading2:"Arial",Heading3:"Arial",Heading4:"Arial"};for(const style of Array.from(doc.getElementsByTagNameNS(W,"style"))){const family=fonts[style.getAttributeNS(W,"styleId")];if(!family)continue;let rPr=Array.from(style.childNodes).find((n)=>n.namespaceURI===W&&n.localName==="rPr");if(!rPr){rPr=wEl(doc,"rPr");style.appendChild(rPr);}let rFonts=Array.from(rPr.childNodes).find((n)=>n.namespaceURI===W&&n.localName==="rFonts");if(!rFonts){rFonts=wEl(doc,"rFonts");rPr.insertBefore(rFonts,rPr.firstChild);}for(const attr of ["ascii","eastAsia","hAnsi","cs"])rFonts.setAttributeNS(W,`w:${attr}`,family);}return new XMLSerializer().serializeToString(doc); }
  function ensureListNumbering(numberingXml) { const doc=xmlDoc(numberingXml),root=doc.documentElement,hasNum=(id)=>Array.from(doc.getElementsByTagNameNS(W,"num")).some((n)=>n.getAttributeNS(W,"numId")===String(id));const addDef=(id,fmt,text)=>{if(hasNum(id))return;const abs=wEl(doc,"abstractNum");abs.setAttributeNS(W,"w:abstractNumId",String(id));const multi=wEl(doc,"multiLevelType");multi.setAttributeNS(W,"w:val","singleLevel");abs.appendChild(multi);const lvl=wEl(doc,"lvl");lvl.setAttributeNS(W,"w:ilvl","0");const start=wEl(doc,"start");start.setAttributeNS(W,"w:val","1");const numFmt=wEl(doc,"numFmt");numFmt.setAttributeNS(W,"w:val",fmt);const lvlText=wEl(doc,"lvlText");lvlText.setAttributeNS(W,"w:val",text);const suff=wEl(doc,"suff");suff.setAttributeNS(W,"w:val","space");const pPr=wEl(doc,"pPr"),ind=wEl(doc,"ind");ind.setAttributeNS(W,"w:left","720");ind.setAttributeNS(W,"w:hanging","360");pPr.appendChild(ind);lvl.append(start,numFmt,lvlText,suff,pPr);abs.appendChild(lvl);root.appendChild(abs);const num=wEl(doc,"num");num.setAttributeNS(W,"w:numId",String(id));const absId=wEl(doc,"abstractNumId");absId.setAttributeNS(W,"w:val",String(id));num.appendChild(absId);root.appendChild(num);};addDef(98,"bullet","•");addDef(99,"decimal","%1.");if(state.docLanguage==="en"&&state.preset==="book-chapter-decimal"){const lvl0=Array.from(doc.getElementsByTagNameNS(W,"lvl")).find((n)=>n.getAttributeNS(W,"ilvl")==="0");if(lvl0){const t=Array.from(lvl0.childNodes).find((n)=>n.namespaceURI===W&&n.localName==="lvlText");if(t)t.setAttributeNS(W,"w:val","Chapter %1");}}if(state.headingsOnly){for(const pStyle of Array.from(doc.getElementsByTagNameNS(W,"pStyle"))){if(/^Heading[1-4]$/.test(pStyle.getAttributeNS(W,"val")||""))pStyle.parentNode.removeChild(pStyle);}}return new XMLSerializer().serializeToString(doc); }
  function buildDocumentXml(originalXml) { const doc=xmlDoc(originalXml),body=doc.getElementsByTagNameNS(W,"body")[0];if(!body)throw new Error("Template body missing");const sectPr=Array.from(body.childNodes).find((n)=>n.namespaceURI===W&&n.localName==="sectPr")?.cloneNode(true)||null;while(body.firstChild)body.removeChild(body.firstChild);if(state.title.trim())body.appendChild(makeParagraph(doc,state.title.trim(),"Title"));for(const node of state.nodes){body.appendChild(makeParagraph(doc,node.title||TEXT.newHeading,`Heading${node.level}`));for(const p of bodyParagraphs(doc,node.body))body.appendChild(p);}if(sectPr)body.appendChild(sectPr);return new XMLSerializer().serializeToString(doc); }
  function patchContentTypes(xml) { return xml.replace(/application\/vnd\.openxmlformats-officedocument\.wordprocessingml\.template\.main\+xml/g,"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"); }
  function patchCoreTitle(coreXml) { try{const doc=xmlDoc(coreXml),title=Array.from(doc.getElementsByTagNameNS("http://purl.org/dc/elements/1.1/","title"))[0];if(title)title.textContent=state.title;return new XMLSerializer().serializeToString(doc);}catch(_){return coreXml;} }
  async function exportWord() { await saveDraftNow();if(!window.JSZip){alert(TEXT.unsupportedZip);return;}const old=el.exportWord.textContent;el.exportWord.disabled=true;el.exportWord.textContent=TEXT.exportPreparing;setStatus(TEXT.exportPreparing);try{const response=await fetch(templateUrl(),{cache:"force-cache"});if(!response.ok)throw new Error(TEXT.templateFetchError);const zip=await JSZip.loadAsync(await response.arrayBuffer());const documentFile=zip.file("word/document.xml"),stylesFile=zip.file("word/styles.xml"),numberingFile=zip.file("word/numbering.xml"),contentTypesFile=zip.file("[Content_Types].xml");if(!documentFile||!stylesFile||!numberingFile||!contentTypesFile)throw new Error("Template package incomplete");const [documentXml,stylesXml,numberingXml,contentTypesXml]=await Promise.all([documentFile.async("string"),stylesFile.async("string"),numberingFile.async("string"),contentTypesFile.async("string")]);zip.file("word/document.xml",buildDocumentXml(documentXml));let patchedStyles=patchEnglishFonts(stylesXml);if(state.headingsOnly)patchedStyles=removeHeadingNumbering(patchedStyles);zip.file("word/styles.xml",patchedStyles);zip.file("word/numbering.xml",ensureListNumbering(numberingXml));zip.file("[Content_Types].xml",patchContentTypes(contentTypesXml));const core=zip.file("docProps/core.xml");if(core)zip.file("docProps/core.xml",patchCoreTitle(await core.async("string")));const blob=await zip.generateAsync({type:"blob",mimeType:"application/vnd.openxmlformats-officedocument.wordprocessingml.document",compression:"DEFLATE",compressionOptions:{level:6}});downloadBlob(blob,`${sanitizeFileName(state.title,TEXT.wordName)}.docx`);setStatus(TEXT.exportDone);}catch(error){console.error(error);alert(`${TEXT.exportError}: ${error.message||error}`);setStatus(TEXT.exportError);}finally{el.exportWord.disabled=false;el.exportWord.textContent=old;} }

  function bindEvents() {
    el.title.addEventListener("input",()=>{state.title=el.title.value;const inline=el.canvas.querySelector(".inline-doc-title");if(inline&&inline!==document.activeElement)inline.value=state.title;const preview=el.canvas.querySelector(".preview-doc-title");if(preview)preview.textContent=state.title;scheduleSave();});
    el.addRoot.addEventListener("click",addRoot);el.addSibling.addEventListener("click",()=>addNode("sibling"));el.addChild.addEventListener("click",()=>addNode("child"));el.promote.addEventListener("click",promote);el.demote.addEventListener("click",demote);el.moveUp.addEventListener("click",moveUp);el.moveDown.addEventListener("click",moveDown);el.split.addEventListener("click",splitSection);el.merge.addEventListener("click",mergePrevious);el.remove.addEventListener("click",deleteSection);
    el.bold.addEventListener("click",()=>applyInline("**"));el.italic.addEventListener("click",()=>applyInline("*"));el.quote.addEventListener("click",()=>applyLinePrefix("quote"));el.bullet.addEventListener("click",()=>applyLinePrefix("bullet"));el.number.addEventListener("click",()=>applyLinePrefix("number"));el.clear.addEventListener("click",()=>applyLinePrefix("clear"));
    el.viewContinuous.addEventListener("click",()=>setView("continuous"));el.viewPages.addEventListener("click",()=>setView("pages"));el.viewFocus.addEventListener("click",()=>setView("focus"));
    el.docLanguage.addEventListener("change",()=>{state.docLanguage=el.docLanguage.value;renderPresetOptions();updateFormatHint();renderOutline();renderDocument();scheduleSave();});el.platform.addEventListener("change",()=>{state.platform=el.platform.value;scheduleSave();});el.preset.addEventListener("change",()=>{state.preset=el.preset.value;renderOutline();renderDocument();updateFormatHint();scheduleSave();});el.headingsOnly.addEventListener("change",()=>{state.headingsOnly=el.headingsOnly.checked;renderOutline();renderDocument();updateFormatHint();scheduleSave();});
    el.newDoc.addEventListener("click",newDocument);el.exportWord.addEventListener("click",exportWord);el.exportJson.addEventListener("click",exportBackup);el.importJson.addEventListener("click",()=>el.importFile.click());el.importFile.addEventListener("change",()=>{const file=el.importFile.files?.[0];if(file)importBackup(file);el.importFile.value="";});
    document.addEventListener("keydown",(event)=>{const mod=event.ctrlKey||event.metaKey;if(mod&&event.key.toLowerCase()==="s"){event.preventDefault();event.shiftKey?exportWord():saveDraftNow();}else if(mod&&event.key==="Enter"){event.preventDefault();addNode(event.shiftKey?"child":"sibling");}else if(event.altKey&&event.key==="ArrowLeft"){event.preventDefault();promote();}else if(event.altKey&&event.key==="ArrowRight"){event.preventDefault();demote();}else if(event.altKey&&event.key==="ArrowUp"){event.preventDefault();moveUp();}else if(event.altKey&&event.key==="ArrowDown"){event.preventDefault();moveDown();}});
    window.addEventListener("scroll",onScroll,{passive:true});window.addEventListener("beforeunload",()=>{try{localStorage.setItem(`${DRAFT_DB}-emergency`,JSON.stringify(state));}catch(_){}});
  }
  async function init() { el.privacy.textContent=TEXT.localOnly;const draft=await loadDraft();if(draft){try{state=normalizeState(draft);}catch(_){}}else{try{const emergency=localStorage.getItem(`${DRAFT_DB}-emergency`);if(emergency)state=normalizeState(JSON.parse(emergency));}catch(_){}}bindEvents();renderAll();setStatus(TEXT.saved); }
  init();
})();