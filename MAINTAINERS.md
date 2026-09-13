# 维护者说明

这个项目的原则是：**普通用户零配置；复杂性留在维护端。**

从 v3.0 起，维护工作还多一条优先级：**稳定接口优先于继续扩张功能。** 公开模板文件名、目录、下载地址与无宏使用方式受 [`STABILITY.md`](STABILITY.md) 约束。

## 发布矩阵

6 种编号方案 × 2 个起步版本 × 2 个平台 = **24 个最终 `.dotx` 模板**。

- 书籍：中文传统 / 章节数字 / 纯数字
- 文章：中文论文 / 数字层级 / 中文简洁
- 起步版本：直接开始 / 带常用结构
- 平台：Windows / macOS

“直接开始版”保持最小内容；“带常用结构版”复用同一编号与平台样式，只增加常见写作骨架与成稿设置。不要把 24 个二进制文件当作 24 份独立源文件手工修改。

## 生成方式

模板由 `python-docx + OOXML` 从代码生成。`build_templates.py` 负责主要结构，`reference_support.py` 负责题注、脚注 / 尾注、参考文献等生成后 OOXML 配置。

本地核心流程：

```bash
pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/reference_support.py
python scripts/verify_templates.py
python scripts/compatibility_check.py
python scripts/manuscript_check.py
python scripts/reference_check.py
python scripts/stability_check.py
python scripts/make_quickstart.py
```

需要检查 README 预览时再运行：

```bash
python scripts/make_previews.py
```

它需要 LibreOffice 与 Noto CJK 字体。

GitHub Actions 会在 `main` 的维护文件发生变化后自动执行生成、校验、24 模板布局冒烟渲染、用户 ZIP 打包、发布包审计，并更新 GitHub Release。

## 两种起步版本

### 直接开始版

稳定路径：

- `templates/<platform>/books/*.dotx`
- `templates/<platform>/articles/*.dotx`

这是 README 和在线选择向导的默认下载目标。打开后只包含标题、一级标题和正文起点，不加入需要额外解释的出版设置。

### 带常用结构版

稳定路径：

- `templates/<platform>/structured/books/*.dotx`
- `templates/<platform>/structured/articles/*.dotx`

书籍版使用三个 Word 节：独立书名页；前言与目录前置部分；正文与后置部分。前置部分页码为小写罗马数字并从 `i` 开始，正文换节后以阿拉伯数字从 `1` 重启。

书籍成稿设置包括：

- `Heading 1` 使用 `pageBreakBefore`，新章节自动另起新页；
- `mirrorMargins` + 约 4 mm gutter，作为通用双面打印 / 装订起点；
- `evenAndOddHeaders`，奇数页页眉读取 `STYLEREF "Heading 1"`，偶数页页眉读取 `STYLEREF "Title"`；
- 正文奇数页页码靠右、偶数页页码靠左，前置部分罗马页码居中；
- 不强制奇数页起章。严格出版物的“右页起章”留给最终排版阶段。

文章版预置作者、单位、日期、摘要、关键词、正文、参考文献，并从阿拉伯数字 `1` 开始显示页码。

两个版本都包含结构标题、摘要、关键词、参考文献、作者信息、日期等辅助样式，因此用户从直接开始版写到一半也能继续扩展结构。

## Word 原生引用能力

所有 24 个模板共享以下能力：

- “图 / 表”题注标签；
- 书籍按一级章编号，文章全文连续编号；
- `Caption` 与“图表来源”样式；
- `Footnote Text / Footnote Reference`；
- `Endnote Text / Endnote Reference`；
- `Bibliography` 与“参考文献条目”悬挂缩进样式。

不要把 Zotero、EndNote 或其他引用管理器嵌入模板。第三方工具继续负责自己的字段、引用规范与刷新；模板只提供兼容的 Word 样式环境。

## 自动检查分层

`verify_templates.py` 检查生成物与项目约定，包括文件数量、模板内容类型、字体、四级编号、快捷键关系、结构样式和常用结构占位内容。

`compatibility_check.py` 在 Windows、macOS 与 Linux runner 上检查：

- 24 个 `.dotx` 的 OOXML 包结构与中文路径；
- 四级标题编号；
- 平台字体；
- 快捷键映射；
- 辅助结构样式；
- VBA 宏缺失。

`manuscript_check.py` 保护成稿 / 打印结构，主要覆盖：

- 书籍结构版的书名页、前置部分和正文分节；
- `lowerRoman` / `decimal` 页码与重启；
- `mirrorMargins`、装订线、奇偶页模式；
- `Heading 1` 自动换页；
- 章节 / 书名 `STYLEREF` 页眉与 `PAGE` 页码；
- 文章作者 / 单位 / 日期与页码结构。

`reference_check.py` 保护题注、交叉引用支持、脚注 / 尾注和参考文献样式，包括平台字体、上标编号和悬挂缩进。

`stability_check.py` 保护 v3 的公开兼容接口：24 个稳定模板路径、稳定整包下载链接、稳定版说明，以及历史维护临时文件不再回流。

主构建工作流还会：

1. 用 LibreOffice 把全部 24 个模板转换为 PDF 做布局冒烟检查；
2. 生成 Windows / macOS 用户 ZIP；
3. 用 `release_audit.py` 验证每个 ZIP 恰好包含 12 个 `.dotx`、快速入门文件，并且没有宏模板、安装程序或意外文件；
4. 通过后才创建 / 刷新 GitHub Release。

这些都属于**结构与布局自动检查**，不会启动 Microsoft Word。不要描述成“所有 Word 版本真机测试通过”。

## 真实 Word 反馈闭环

真实使用反馈分两条路径：

- `.github/ISSUE_TEMPLATE/word_quick_success.yml`：几十秒轻量正常反馈；
- `.github/ISSUE_TEMPLATE/word_compatibility_report.yml`：3～5 分钟完整真机验证；
- `docs/真实Word验收.md`：普通用户测试步骤；
- `docs/兼容性验证记录.md`：按平台、Word 版本、编号方案和起步版本维护公开记录。

标题前缀作为维护索引：

- `[Word 正常]`：轻量正常反馈；
- `[Word 验证]`：完整真机验证；
- `[Word 兼容性]`：旧版兼容性入口。

完整验证的四个关键项是：打开模板、多级标题、正文输入、保存重开。四项全部正常时可以记录“关键项正常”；任一项有问题就记录“有问题”并保留 Issue 链接。目录、成稿 / 打印版式、题注 / 引用、脚注 / 参考文献、导航窗格与快捷键属于补充项。

轻量反馈只证明“这个用户实际用过，目前没发现明显问题”，不能替代完整验证。

## 记录原则

维护真实 Word 反馈时：

1. 不要求用户提供个人信息或真实写作内容；
2. 只记录公开 Issue 明确提供的信息；
3. 不把轻量反馈写成完整验收；
4. 不把自动结构检查写成 Microsoft Word 真机测试；
5. 不使用“完全兼容所有 Word 版本”等无法证明的措辞。

## v3 版本策略

根目录 `version.txt` 是唯一发布版本号来源。

3.x 采用以下约定：

- **补丁版本**：修复问题、文档、CI、兼容性，不改变公开路径和核心行为；
- **小版本**：兼容地增强已有能力，但不能要求普通用户改变下载 / 打开方式；
- **主版本**：只有需要破坏稳定接口时才考虑，例如重命名模板、改变编号体系、改变 Release 资产名或引入新的用户运行依赖。

已经保存成 `.docx` 的文稿不是模板的运行依赖，因此模板升级不要求用户给旧文稿“重新套模板”。如果某次发布确实建议重新下载，会在 Release 说明中明确写出。

发布前至少确认：

- `CHANGELOG.md` 已更新；
- `version.txt` 已更新；
- `STABILITY.md` 没有被新功能违反；
- PR 的三平台兼容检查通过；
- 合并后的主构建、布局冒烟、release audit 和 Release 创建全部通过。

## 快捷键内部逻辑

同一组 Word 键位定义在两个平台分别表现为：

- Windows：`Ctrl + Alt + ...`
- macOS：`Command + Option + ...`

最终仍分开发布两个平台的模板，因为中文字体不同，而且分平台下载对普通用户更清楚。

## Toolbox 集成边界

`SeekerThinker/toolbox` 只负责项目索引和在线模板选择入口；模板源码、Release、Issues、兼容性记录都留在独立仓库。不要把 24 个二进制模板复制进 Toolbox。

Toolbox 使用稳定的 `releases/latest` 下载链接和 `main/templates/...` 单模板路径。3.x 正是为了让这些入口在小版本升级时无需同步修改。
