# 维护者说明

项目始终遵循：**普通用户零配置；复杂性留在维护端。** 优先顺序为 **思考 → 结构 → 记录 / 写作 → 排版**。整理笔记与材料本身是完整用途，正式成稿不是默认终点。用户现在有两条独立起点：网页在线整理并导出 Word，或者直接下载 `.dotx` 在 Word 中工作；不要让其中一条依赖另一条。

当前项目决定见 [docs/项目决策.md](docs/项目决策.md)；稳定接口见 [STABILITY.md](STABILITY.md)；贡献与实际命令见 [CONTRIBUTING.md](CONTRIBUTING.md)；AI 协作约定见 [AGENTS.md](AGENTS.md)。

## 公共产品矩阵与生成路径

**6 种编号 × Windows/macOS = 12 个用户 `.dotx`**。书籍：中文传统 / 章节数字 / 纯数字；文章：中文论文 / 数字层级 / 中文简洁。公共路径为 `templates/<platform>/books/*.dotx`、`templates/<platform>/articles/*.dotx`，每个平台 Release ZIP 仅包含 6 个。v3 的 `templates/<platform>/structured/...` 可能继续由生成器产生，但只是内部过渡副本，不在 v4 用户矩阵和下载包中。

模板由 `python-docx + OOXML` 从代码生成；维护时改生成器及后处理，不直接手改公共 `.dotx`。主链条包含：

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

`thinking_support.py` 保持「标题层级 + 导航窗格」提示与可选成稿区块不进大纲，并将统一模板提升至公共短路径。`reference_support.py` 管理题注、脚注/尾注及参考文献样式。`thinking_check.py`、`manuscript_check.py`、`stability_check.py` 检查公共 12 模板；部分兼容性检查仍遍历历史内部产物，但不要因此把用户模板总数写成 24。

公共模板的前言、目录、作者信息、摘要、附录和参考文献属于可选成稿能力，`结构标题` 等辅助内容必须使用非大纲级别；真正标题 1–4 才进入 Word 导航窗格。书籍分节符与罗马 / 阿拉伯页码、奇偶页页眉相连；删前置文字通常可行，大幅删除前置部分时应避免误删关键分节符。保留原生 Caption、Footnote Text / Reference、Endnote Text / Reference、Bibliography 等样式；不要在模板里改写 Zotero / EndNote 等第三方字段。

## 网页编辑器与数据边界

`site/editor.js` 是共用的网页数据模型与 `.docx` 导出实现，`site/editor-copy.js` 提供中英文表达，`site/i18n.js` 负责页面语言切换；中英文编辑器页面共用功能代码。在线编辑器**默认全文可编辑**，左侧标题树与正文双向定位；专注模式可选，页面预览只读且不保证 Word 精确分页。

当前草稿 v3 由章节文本块、表格块和独立脚注对象组成。旧 v2 `body` 字符串应能迁移；改模型时必须验证旧 JSON 恢复、表格与脚注、文本引用和本地保存。当前草稿优先存于浏览器 IndexedDB，失败时尝试 localStorage：它不是云端同步或可靠的唯一备份。用户可下载 JSON 恢复项目，另导出 `.docx` 在 Word 中继续；**不承诺任意 Word 文件无损导入网页**。

导出读取与页面同源提供的 12 个 `.dotx` 骨架，保留 Word 样式、编号与布局等 OOXML 部件；导出中的 `w:tbl`、脚注关系和 `word/footnotes.xml` 应是真实部件。不能仅靠肉眼看网页像表格或脚注就宣称 Word 原生兼容。文稿不为导出而上传项目服务器；但 JSZip 的受完整性校验脚本目前从外部 CDN 获取，不能声称整站完全离线运行。详见 [在线编辑器说明](docs/在线编辑器.md)。

## 中英文、快捷键与测试

公共主页、编辑器、Word 使用说明和新用户指南按 [双语维护约定](docs/双语维护.md) 同步。中文产品语义为基准，英文可自然表达但不能漏掉警示与功能；**界面语言、文档语言、编号方案各自独立**。不要把「中文传统章节编号」译成含糊的 “Traditional Chinese”。历史中文内部维护文件并非全部已经双语，不能夸称仓库全面双语。

网页与 Word 共用标题 1–4、正文、表格、引用、脚注样式快捷键；网页独有的结构操作另列。改变快捷键须同时检查模板 customizations、网页键盘事件与两种语言说明。视图说明动态文案不得在 MutationObserver 回调中无条件重写自身；`node scripts/editor_copy_check.cjs` 检查中英文视图更新不会自触发循环。

CI 至少覆盖 `node --check`、上述视图回归、`scripts/web_editor_export_check.py` 的 12 模板 Word 包检查、双语入口契约和 Pages 静态站组装。用户矩阵与发布 ZIP 还有独立模板构建、PDF 布局冒烟和 release audit。**这些检查不等于真实浏览器交互，也不等于在 Microsoft Word 真机上完成验收**。对外报告必须分别说明哪些已跑、哪些未跑。真实反馈仅记录用户在公开 Issue 主动提供的信息，不索取个人信息或私人文稿。

## 发布与版本约定

从最新 `main` 创建分支再写入，检查 PR diff、CI 后才合并；不要写入 `main` 来探测分支。自动模板构建可能在合并后更新 `main`，下一次工作必须重新获取 SHA。根目录 `version.txt` 是模板发布版本唯一来源；编辑器或文案的小改动不应自动提升模板版本。

4.x 补丁版本可修兼容性、文档、CI 和体验；兼容新增功能可考虑小版本；改变稳定文件名、编号、资产名或运行方式需要另行评估主版本。发布前核对 [STABILITY.md](STABILITY.md)、12 模板、Windows/macOS ZIP、真实行为表述与双语一致性。

站点首页 `https://seekerthinker.github.io/word-writing-templates/` 为普通用户入口；其他项目可链接过来，但不应维护第二套独立模板矩阵或产品文案。**复杂性留在维护端，结构留在用户眼前。**
