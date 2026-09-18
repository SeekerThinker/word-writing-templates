(() => {
  "use strict";

  const isEn = (document.documentElement.lang || "").toLowerCase().startsWith("en");
  const text = isEn ? {
    title: "Online structured thinking & writing | Structured Thinking & Writing with Word",
    description: "Keep the whole structure visible while ideas grow in the document body. Organize with heading levels, reshape the whole, and export the same structure—including real tables and footnotes—to Word when you are ready to continue there.",
    brand: "Online thinking & writing",
    eyebrow: "Think → organize → write",
    heading: "Keep the structure in view.\nLet the writing keep growing.",
    intro: "Write first, then use headings to name, group, and place what you have. The outline keeps the whole document visible while the body holds the detail. Work on one passage, step back to inspect the whole, rename, move, split, or merge, then return to the text. When you are ready for Word, export the same structure and continue there without rebuilding it.",
    platform: "Continue in Word on",
    preset: "Word numbering & layout",
    outlineTitle: "Structure",
    outlineHint: "Keep the whole in view; drag a heading to move its section",
    continuous: "Develop the passage in front of you while keeping the whole document visible. Use the outline to move naturally between the part and the whole.",
    pages: "Step back into a paper-like view to inspect length and shape. Pagination here is an approximation; Word remains the final reference after export.",
    focus: "Set the rest aside for a moment and keep only the current section and its subsections in view. Return to the full document whenever you want the whole structure back.",
    syntax: "Keep the body lightweight while ideas are still moving: **bold**, *italic*, > for a quote, - for bullets, and 1. for a numbered list. Tables and footnotes are real document objects, and all of these continue into Word on export.",
    shortcutIntro: "Heading levels, body text, quotes, tables, and footnotes use the same shortcuts here and in the Word template. Learn them once here, then carry the same habits into Word.",
    sharedShortcuts: "Carry the same shortcuts into Word",
    webShortcuts: "Browser-only structure commands",
    sharedNote: "Tables and footnotes are not temporary marks: they export as real Word tables and footnotes, alongside the same heading hierarchy.",
    privacy: "Your draft stays in this browser by default and is not uploaded to the project server. Use this space to think, organize, and write; when you move into Word, the same heading hierarchy, tables, and footnotes can continue with you. Page preview is for seeing the whole; final pagination is determined by Word."
  } : {
    title: "在线结构化思考与写作｜Word 结构化思考与写作",
    description: "让标题层级承载想法之间的关系，让整体始终可见，在正文中记录与展开；需要进入 Word 时，再把同一套结构连同真正的表格和脚注一起导出并继续写作。",
    brand: "在线结构化思考与写作",
    eyebrow: "思考 → 组织 → 写作",
    heading: "让结构始终可见，\n让想法在正文里继续生长。",
    intro: "先把想法写下来，再用标题为它们命名、分层，并找到彼此的位置。左边保留整体，右边承载具体的记录与展开；在局部写一点，再退回来看看全局，改名、移动、拆分或合并以后，再回到正文继续。需要进入 Word 时，同一套结构可以直接带过去，不必重新搭一遍。",
    platform: "之后在哪个平台继续使用 Word",
    preset: "Word 编号与版式",
    outlineTitle: "结构",
    outlineHint: "让整体始终在眼前；拖动标题即可移动整节",
    continuous: "在正文里展开眼前的内容，也让整篇文档保持可见；借助左侧结构，在局部与整体之间来回。",
    pages: "退后一步，用接近纸张的视野观察全文的篇幅与形态。这里的分页只是近似预览，最终仍以导出后的 Word 为准。",
    focus: "暂时收起其余内容，只留下当前一节和它的下级标题；需要重新判断全局时，再回到全文。",
    syntax: "想法还在生长时，正文可以保持轻量：**加粗**、*斜体*、行首 > 引用、- 项目符号、1. 编号列表。表格和脚注则是真正的文档对象，导出后会继续成为 Word 中的表格和脚注。",
    shortcutIntro: "标题层级、正文、引用、表格与脚注，在网页和 Word 中沿用同一套快捷键。先在这里形成习惯，导出以后不必再换一套操作方式。",
    sharedShortcuts: "从网页一路用到 Word",
    webShortcuts: "只在网页里使用的结构操作",
    sharedNote: "表格和脚注不是临时标记：它们会连同标题层级一起，作为真正的 Word 表格和脚注进入导出的文档。",
    privacy: "文稿默认只保存在这个浏览器中，不会上传到项目服务器。你可以在这里思考、整理和写作；需要进入 Word 时，标题层级、表格与脚注会沿着同一份文档继续下去。页面预览用于看整体，最终分页仍以 Word 为准。"
  };

  document.title = text.title;
  const meta = document.querySelector('meta[name="description"]');
  if (meta) meta.setAttribute("content", text.description);

  const brand = document.querySelector(".editor-brand-copy small");
  if (brand) brand.textContent = text.brand;

  const intro = document.querySelector(".editor-intro > div:first-child");
  if (intro) {
    let eyebrow = intro.querySelector(".editor-copy-eyebrow");
    if (!eyebrow) {
      eyebrow = document.createElement("p");
      eyebrow.className = "editor-copy-eyebrow";
      intro.insertBefore(eyebrow, intro.firstChild);
    }
    eyebrow.textContent = text.eyebrow;
    const heading = intro.querySelector("h1");
    if (heading) {
      heading.textContent = "";
      const parts = text.heading.split("\n");
      parts.forEach((part, index) => {
        if (index) heading.appendChild(document.createElement("br"));
        heading.appendChild(document.createTextNode(part));
      });
    }
    const paragraph = intro.querySelector("p:not(.editor-copy-eyebrow)");
    if (paragraph) paragraph.textContent = text.intro;
  }

  const platformLabel = document.querySelector('label[for="platform"]');
  if (platformLabel) platformLabel.textContent = text.platform;
  const presetLabel = document.querySelector('label[for="preset"]');
  if (presetLabel) presetLabel.textContent = text.preset;

  const panelHead = document.querySelector(".outline-panel .panel-head > div");
  if (panelHead) {
    const strong = panelHead.querySelector("strong");
    const small = panelHead.querySelector("small");
    if (strong) strong.textContent = text.outlineTitle;
    if (small) small.textContent = text.outlineHint;
  }

  const viewNote = document.querySelector("#viewNote");
  const viewCopy = () => {
    const active = document.querySelector('.view-switch button[aria-pressed="true"]')?.id;
    if (!viewNote) return;
    const next = active === "viewPages" ? text.pages : active === "viewFocus" ? text.focus : text.continuous;
    // The editor rewrites this note when switching modes. Do not rewrite our
    // own identical text: that would retrigger the observer indefinitely.
    if (viewNote.textContent !== next) viewNote.textContent = next;
  };
  if (viewNote) {
    const observer = new MutationObserver(viewCopy);
    observer.observe(viewNote, { childList: true, characterData: true, subtree: true });
    document.querySelectorAll(".view-switch button").forEach((button) => button.addEventListener("click", () => requestAnimationFrame(viewCopy)));
    viewCopy();
  }

  const syntax = document.querySelector(".syntax-help");
  if (syntax) syntax.textContent = text.syntax;

  const shortcut = document.querySelector("#shortcutPanel .shortcut-content");
  if (shortcut) {
    const introCopy = shortcut.querySelector(":scope > p");
    if (introCopy) introCopy.textContent = text.shortcutIntro;
    const groups = shortcut.querySelectorAll(".shortcut-group");
    if (groups[0]) {
      const h3 = groups[0].querySelector("h3");
      const note = groups[0].querySelector(".shortcut-platform-note");
      if (h3) h3.textContent = text.sharedShortcuts;
      if (note) note.textContent = text.sharedNote;
    }
    if (groups[1]) {
      const h3 = groups[1].querySelector("h3");
      if (h3) h3.textContent = text.webShortcuts;
    }
  }

  const privacy = document.querySelector(".editor-note");
  if (privacy) privacy.textContent = text.privacy;

  const style = document.createElement("style");
  style.textContent = `
    .editor-copy-eyebrow {
      margin: 0 0 10px;
      color: var(--accent, #2d5a4a);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: .11em;
    }
    .editor-intro > div:first-child > p:not(.editor-copy-eyebrow) {
      max-width: 820px;
      line-height: 1.82;
    }
  `;
  document.head.appendChild(style);
})();