# 维护者说明

这个项目的原则是：**普通用户零配置；复杂性留在维护端。**

v4 的产品目标进一步明确：**一个编号方案只对应一个用户模板。** 思考阶段和成稿阶段使用同一份 Word 文件，不再让普通用户判断“直接开始版”还是“带常用结构版”。

## 用户产品矩阵

6 种编号方案 × 2 个平台 = **12 个用户 `.dotx` 模板**。

- 书籍：中文传统 / 章节数字 / 纯数字
- 文章：中文论文 / 数字层级 / 中文简洁
- 平台：Windows / macOS

公共路径：

- `templates/<platform>/books/*.dotx`
- `templates/<platform>/articles/*.dotx`

v4 初期旧生成器仍会产生 `templates/<platform>/structured/...` 副本，作为内部过渡产物。`thinking_support.py` 会把完整结构版本提升到上面的公共短路径。历史副本**不进入 Release ZIP，也不属于 v4 用户矩阵**。

## 核心产品原则

产品优先级始终是：**思考 → 结构 → 写作 → 排版。**

公共模板必须同时满足两点：

1. 已经准备好作者信息、前言 / 摘要、目录、参考文献、页码等成稿能力；
2. 这些可选成稿区块不能污染导航窗格的思考树。

因此 `结构标题` 必须使用非大纲级别；`标题 1 / 2 / 3 / 4` 才是导航窗格里的主要结构。

## 生成方式

模板由 `python-docx + OOXML` 从代码生成。

核心流程：

```bash
pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/thinking_support.py
python scripts/reference_support.py
python scripts/verify_templates.py
python scripts/compatibility_check.py
python scripts/thinking_check.py
python scripts/manuscript_check.py
python scripts/reference_check.py
python scripts/stability_check.py
python scripts/make_quickstart.py
```

`thinking_support.py` 在 v4 有两项职责：

- 加入“标题层级 + 导航窗格”的轻量思考提示，并确保可选结构标题不进入导航窗格；
- 将完整结构模板提升到稳定的短文件名，使用户只看到一个模板版本。

`reference_support.py` 继续负责题注、脚注 / 尾注、Bibliography 与参考文献样式等 OOXML 配置。

## 自动检查

`compatibility_check.py` 仍会检查生成器的全部内部产物，以防 v3 过渡构建链悄悄损坏。

`thinking_check.py` 专门保护 v4 的**12 个公共模板**：

- 必须包含标题层级 + 导航窗格思考提示；
- 书籍 / 文章的可选成稿结构必须存在；
- `结构标题` 必须使用 outline level 9，不进入导航窗格。

`manuscript_check.py` 只以 12 个公共模板为产品对象，检查书籍分节、页码、打印设置、页眉页脚，以及文章元信息和页码。

`reference_check.py` 检查题注、交叉引用支持、脚注 / 尾注、Bibliography 和“参考文献条目”等样式。

`stability_check.py` 保护 v4 的 12 个公共模板路径、两个稳定 `releases/latest` 下载地址和“一套模板，两种使用深度”的产品原则。

主构建会把 **12 个用户模板**转换为 PDF 做布局冒烟测试。用户 ZIP 每个平台只允许 6 个 `.dotx`；`release_audit.py` 会拒绝多余模板、宏模板、安装程序或意外文件。

这些自动检查**不会启动 Microsoft Word**。不要把它们描述成真实 Word 真机验证。

## 书籍模板的删除安全

书籍模板包含书名页、前置部分和正文的 Word 分节，用于维持罗马页码、正文重新从 `1` 开始和不同页眉页脚。

所以文档和提示应鼓励用户：

- 暂时不用的前言 / 目录 / 附录 / 参考文献可以先保留；
- 删除这些区块的文字通常安全；
- 大幅删除前置部分时要避免误删正文前的分节符。

不要为了“看起来更简洁”而把分节符等关键结构变成需要普通用户自己重新建立的东西。

## Word 原生引用能力

所有公共模板共享：

- “图 / 表”题注标签；
- 书籍按一级章编号，文章全文连续编号；
- `Caption` 与“图表来源”样式；
- `Footnote Text / Footnote Reference`；
- `Endnote Text / Endnote Reference`；
- `Bibliography` 与“参考文献条目”悬挂缩进样式。

不要把 Zotero、EndNote 或其他引用管理器嵌入模板。第三方工具继续负责自己的字段、引用规范与刷新；模板只提供兼容的 Word 样式环境。

## 真实 Word 反馈闭环

真实使用反馈继续分两条路径：

- `.github/ISSUE_TEMPLATE/word_quick_success.yml`：几十秒轻量正常反馈；
- `.github/ISSUE_TEMPLATE/word_compatibility_report.yml`：3～5 分钟完整真机验证。

维护公开兼容性记录时：

1. 不要求用户提供个人信息或真实写作内容；
2. 只记录公开 Issue 明确提供的信息；
3. 不把轻量反馈写成完整验收；
4. 不把自动结构检查写成 Microsoft Word 真机测试；
5. 不使用“完全兼容所有 Word 版本”等无法证明的措辞。

## v4 版本策略

根目录 `version.txt` 是唯一发布版本号来源。

4.x 采用以下约定：

- **补丁版本**：修复兼容性、文档、CI、布局和小范围体验问题；
- **小版本**：兼容地增强已有能力，但不能重新增加用户模板选择负担；
- **主版本**：只有需要破坏稳定用户文件名、编号方案、Release 资产名或运行方式时才考虑。

已经保存成 `.docx` 的文稿不是模板的运行依赖，因此模板升级不要求给旧文稿“重新套模板”。v3.0.1 Release 保留旧的双版本工作流，v4 不要求旧用户迁移。

发布前至少确认：

- `version.txt` 与 Release 目标一致；
- `STABILITY.md` 没有被新功能违反；
- PR 的 Windows / macOS / Linux 检查通过；
- 合并后的 12 模板布局冒烟、release audit 和 Release 创建全部通过；
- 对真实 Word 行为的表述仍然克制、可验证。

## Toolbox 集成边界

`SeekerThinker/toolbox` 只负责项目索引和在线模板选择入口；模板源码、Release、Issues、兼容性记录都留在独立仓库。

Toolbox 应只暴露 v4 的 12 个公共模板，不再提供“直接开始版 / 带常用结构版”两个下载按钮。
