# 参与贡献

感谢你愿意改进这个项目。它既提供可直接在 Word 使用的模板，也提供先在浏览器里整理、记录和写作，再导出 Word 的编辑器。我们优先保护**思考 → 结构 → 记录 / 写作 → 排版**这条工作路径；普通用户零配置，复杂性留在维护端。

[English contribution guide](CONTRIBUTING.en.md) · [项目主页](https://seekerthinker.github.io/word-writing-templates/) · [稳定承诺](STABILITY.md)

## 可以贡献什么

欢迎修正文档与中英文翻译、报告 Windows/macOS 不同 Word 版本的兼容问题、改善标题层级和网页全文章节导航、修复表格与脚注导出、增强无须上传私人文稿的自动化检查。请不要把“所有记录最终必须成稿”当作产品前提，也不要为了增加功能让普通用户额外安装软件。

## 修改前先确认

先读 `README.md`、`STABILITY.md`、`MAINTAINERS.md`；涉及网页编辑器，再读 `docs/在线编辑器.md`。如借助 AI 协作，读 `AGENTS.md`。**从最新 `main` 创建工作分支后再写入**，不要在 `main` 上放临时文件或用写入测试分支是否存在；提交 PR，核对 diff 中是否包含意外的模板、下载文件或私人草稿。用户文件、私人文稿和支付凭据不得纳入仓库。

现行 v4 **用户产品矩阵为 6 种编号 × 2 平台 = 12 个 `.dotx`**。内部构建可能仍产生 v3 历史兼容副本；不要把它们误写成 24 个用户模板。发布 ZIP 每个平台仅包含 6 个公共模板。公共文件名、路径、稳定 Release 下载地址和无宏体验受 `STABILITY.md` 保护。

## 检查与提交

模板和 Open XML 相关变更，先安装依赖并运行相应检查：

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/thinking_support.py
python scripts/reference_support.py
python scripts/verify_templates.py
python scripts/compatibility_check.py
python scripts/thinking_check.py
python scripts/manuscript_check.py
python scripts/reference_check.py
python scripts/stability_check.py
python scripts/web_editor_export_check.py
```

网页编辑器或双语站点变更，至少执行：

```bash
node --check site/editor.js
node --check site/editor-copy.js
node --check site/i18n.js
node --check site/app.js
node --check site/en/app.js
node scripts/editor_copy_check.cjs
python scripts/web_editor_export_check.py
```

模板生成后的主构建还会运行 PDF 布局冒烟测试、下载包审计和 Windows/macOS/Linux 相关检查。**OOXML / PDF 自动检查不等于真实 Microsoft Word 真机验收**。如验证的是具体 Word 版本，请写明操作系统、Word 版本、模板或导出文件、复现步骤及实际观察，不要上传真实私人文稿。

涉及浏览器交互（全文章节定位、视图切换、键盘输入、本地保存、表格、脚注、下载）时，应另外做浏览器实际操作测试；只通过 `node --check` 或检查 HTML 文本并不能证明交互正常。浏览器测试未运行就明确标注未运行。

涉及备份数据结构时，检查旧 v2 `body` 到 v3 文本块的迁移、JSON 导入与导出、表格/脚注保留，并确认当前草稿不因升级被静默覆盖。不要将 `.docx` 描述为可以直接导回网页的项目备份；恢复网页草稿使用 JSON。

## 双语与 PR 说明

公共主页、编辑器和使用说明有中英文页面。改动一边的功能、隐私声明、警告、快捷键或步骤时，应在同一 PR 同步另一边，按 [双语维护约定](docs/双语维护.md) 检查语义而非逐字相同。中文产品原则和术语为语义基准；英文应自然准确。技术文件可保持单份，不能因此漏掉面向用户的英文说明。现有历史中文维护文档暂不宣称已经全部双语。

PR 请说明改了什么、为何不破坏现有模板与用户草稿、运行了哪些测试，以及哪些测试（尤其真机 Word 或真实浏览器）没有运行。不要手改 `templates/` 生成品来代替生成逻辑；不要加入 VBA 宏、安装程序、付费门槛或无关依赖。
