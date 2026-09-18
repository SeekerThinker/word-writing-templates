# AI 协作与接手约定 / AI collaboration guide

> 本文件仅约束**维护本仓库的协作方式**，不是要求普通用户遵循研究协议，也不表示网页编辑器内置 AI 写作。项目状态以最新 GitHub 仓库为准；聊天摘要、AI 建议或旧上下文不能替代仓库文件。
>
> This file governs repository maintenance only. It does not impose a research protocol on users or imply that the browser editor includes AI writing. The latest repository state, not chat history, is authoritative.

## 接手时先读 / Start here

1. 读取最新 `main`，确认分支、开放 PR 和 CI 状态；不要沿用聊天里记下的 SHA。 / Fetch current `main`, open PRs, and CI; never reuse a remembered SHA.
2. `README.md` / `README.en.md`：产品目的与两条用户路径。 / Product purpose and both entry paths.
3. `STABILITY.md`、`MAINTAINERS.md`：模板公共接口与维护边界。 / Stable template contracts and maintainer constraints.
4. `docs/项目决策.md`：已确认的持久选择、仍待决定的事项。 / Adopted decisions and unresolved items.
5. 按任务读源码和说明：网页 `site/editor.js`、`site/editor-copy.js`、`docs/在线编辑器.md`；模板 `scripts/` 与生成器；双语 `docs/双语维护.md`。 / Read task-relevant sources, not the whole repo indiscriminately.

## 人的决定、AI 的建议 / Human decisions versus AI proposals

用户明确采纳的方向才能写入 `docs/项目决策.md` 的「已确认」；AI 提出但未被用户接受的方案只放在「待决定」，不得当成需求实施。不要把文字润色当作改变产品含义的许可。 / Only explicitly accepted user directions are adopted decisions. Unaccepted AI suggestions remain proposals, not product requirements.

维护中区分：**产品与内容**（要实现什么、服务哪些用途）、**表达与版式**（文案、语言、视觉）、**协作与发布**（分支、校验、验收）。改动会影响稳定接口、隐私、付费收款或用户数据时，先核对既有决定与事实；不凭猜测创建支付链接、数据同步或承诺完全兼容。 / Keep product meaning, presentation, and release procedures distinct. Never invent payment destinations, cloud sync, or universal compatibility.

## 写入与发布 / Write and release

- 先从**最新 `main` 建分支**，再做任何写入；禁止直接在 `main` 写测试文件、探测分支或修改生成模板。 / Create a branch before the first write; never probe branches by writing to `main`.
- 先改权威生成逻辑或源文件，再更新相应文档、中英文页面与测试；不要仅手工改生成的 `.dotx`。 / Update source and generator first, then corresponding documents and tests.
- PR 必须检查 diff、旧草稿兼容、12 个公开模板与稳定下载路径；通过 CI 才考虑合并。 / Review the diff, draft compatibility, 12 public templates, and download paths; merge only after checks pass.
- **报告验证层级**：语法 / 静态检查、真实 OOXML 生成与读取、GitHub Pages 部署、真实浏览器交互、真实 Microsoft Word 操作是不同证据。没有做过的不要声称做过。 / Distinguish static checks, OOXML validation, Pages deployment, browser interaction, and actual Word testing.
- 不把私人文稿、浏览器草稿、密钥、收款信息或未经授权的外部内容加入仓库。 / Never commit private writing, draft data, secrets, or unapproved payment information.

## 双语与复杂度 / Bilingual scope and complexity

站点首页、编辑器、使用说明及新公共使用指南保持中英文语义对应；中文产品定位是概念基准，英文应自然准确。技术代码可以保持一份；历史中文维护文件不声称已全部双语。参见 `docs/双语维护.md`。 / Keep public user-facing experiences semantically aligned in Chinese and English; historical maintainer docs are not all mirrored.

**普通用户零配置；复杂性留在维护端。** 不照搬外部研究协议的多级审批、工作记忆和强制接管报告，也不要求用户接触 GitHub。若本文件与用户明确的新决定或 `STABILITY.md` 冲突，先核对并更新相应权威文件，而非静默覆盖。 / Keep governance lightweight; do not transplant mandatory research-protocol machinery into the user interface.

参考启发 / Inspiration: [Human–AI Research Collaboration Protocol](https://github.com/ChongLiuPhil/Human-AI-Research-Collaboration-Protocol). 本项目仅借鉴仓库持久记录与人类决定可追溯的原则，**不宣称实现或符合 HARC 协议**。 / Inspired by its repository-backed continuity; this project does **not** claim HARC compliance.
