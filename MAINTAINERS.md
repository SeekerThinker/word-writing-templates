# 维护者说明

这个项目的原则是：**普通用户零配置；复杂性留在维护端。**

## 发布矩阵

6 种编号方案 × 2 个起步版本 × 2 个平台 = 24 个最终 `.dotx` 模板。

- 书籍：中文传统 / 章节数字 / 纯数字
- 文章：中文论文 / 数字层级 / 中文简洁
- 起步版本：直接开始 / 带常用结构
- 平台：Windows / macOS

“直接开始版”保持最小内容；“带常用结构版”复用同一编号与平台样式，只增加常见写作骨架与成稿设置。因此维护时不要把它们当成两套独立源文件手工修改。

## 生成方式

模板由 `python-docx + OOXML` 从代码生成。修改字体、编号、快捷键、通用样式、分节、页码、页眉、打印设置或占位内容时，只需要修改生成逻辑，再统一生成全部成品。

```bash
pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/verify_templates.py
python scripts/compatibility_check.py
python scripts/manuscript_check.py
python scripts/make_quickstart.py
```

GitHub Actions 会在 `main` 的维护文件发生变化后自动执行生成、校验、布局冒烟渲染、打包，并更新 GitHub Release。

## 两种起步版本

### 直接开始版

路径保持稳定：

- `templates/<platform>/books/*.dotx`
- `templates/<platform>/articles/*.dotx`

这是 README 和在线选择向导的默认下载目标，打开后只包含标题、一级标题和正文起点。除通用的标题 / 正文分页保护外，不给它加入镜像页边距、奇偶页眉等需要解释的出版设置。

### 带常用结构版

路径：

- `templates/<platform>/structured/books/*.dotx`
- `templates/<platform>/structured/articles/*.dotx`

书籍版使用三个 Word 节：独立书名页；前言与目录前置部分；正文与后置部分。前置部分页码为小写罗马数字并从 `i` 开始，正文换节后以阿拉伯数字从 `1` 重启。

v2.7 的书籍成稿设置还包括：

- `Heading 1` 使用 `pageBreakBefore`，新章节自动另起新页；
- `mirrorMargins` + 约 4 mm gutter，用作通用双面打印 / 装订起点；
- `evenAndOddHeaders`，奇数页页眉读取 `STYLEREF "Heading 1"`，偶数页页眉读取 `STYLEREF "Title"`；
- 正文奇数页页码靠右、偶数页页码靠左，前置部分罗马页码保持居中；
- 不自动强制奇数页起章。严格出版物的“右页起章”应由最终排版阶段按要求加入奇数页分节符。

文章版预置作者、单位、日期、摘要、关键词、正文、参考文献，并从阿拉伯数字 `1` 开始显示页码。v2.7 只调整第一页的标题与元信息间距，不增加新产品变体。

两个版本都包含 `结构标题`、`目录标题`、`摘要`、`关键词`、`参考文献`、`模板提示`、`作者信息`、`日期` 等辅助样式，因此用户从直接开始版写到一半也能继续扩展结构。

## 自动检查分层

`verify_templates.py` 检查生成物与项目约定是否一致，包括文件数量、模板内容类型、字体、四级编号、快捷键关系、结构样式和常用结构占位内容。

`compatibility_check.py` 尽量只依赖 Python 标准库，因此会在 GitHub Actions 的 Windows、macOS 与 Linux runner 上运行同一套跨平台检查，主要覆盖：

- 24 个 `.dotx` 的 OOXML 包结构与中文路径；
- 四级标题编号；
- Windows / macOS 平台字体；
- 快捷键映射；
- 辅助结构样式；
- 宏文件缺失检查。

`manuscript_check.py` 专门保护成稿 / 打印结构，当前主要检查：

- 书籍结构版至少包含书名页、前置部分、正文三个节；
- 前置部分存在 `lowerRoman` 页码，正文存在 `decimal` 页码，并分别从 `1` 开始；
- `mirrorMargins`、装订线、奇偶页模式存在；
- `Heading 1` 存在自动换页与 `keepNext`；
- 奇数页章节页眉、偶数页书名页眉以及前置 / 正文页码字段存在；
- 文章结构版存在作者 / 单位 / 日期占位、对应样式与从 `1` 开始的 `PAGE` 页码。

主构建工作流还会用 LibreOffice 把全部 24 个成品模板转换为 PDF，作为布局冒烟检查。它能发现无法渲染、明显分页或字体问题，但依然不等于 Microsoft Word 真机测试。

这些都属于**结构与布局自动检查**，不会启动 Microsoft Word。不要在文档或 Release 说明中把它描述成“所有版本 Word 真机测试通过”。真实 Word 版本、输入法、插件、系统快捷键、字段刷新和打印驱动仍应通过实际使用反馈补充验证。

## 真实 Word 反馈闭环

真实使用反馈分成两条路径：

- `.github/ISSUE_TEMPLATE/word_quick_success.yml`：几十秒的轻量正常反馈；
- `.github/ISSUE_TEMPLATE/word_compatibility_report.yml`：3～5 分钟的完整真机验证；
- `docs/真实Word验收.md`：给普通用户看的测试步骤；
- `docs/兼容性验证记录.md`：按平台、Word 版本、编号方案和起步版本维护公开矩阵。

v2.7 起，完整验证中的“成稿 / 打印版式”补充项应特别观察：新增“标题 1”是否自动换页、奇偶页页眉是否不同、正文页码是否在外侧，以及镜像页边距在打印布局中是否符合预期。

标题前缀作为维护时的稳定索引：

- `[Word 正常]`：轻量正常反馈；
- `[Word 验证]`：新版完整真机验证；
- `[Word 兼容性]`：v2.4 及更早的旧版入口。

### 处理完整真机验证

新版表单要求用户分别填写四个关键项：打开模板、多级标题、正文输入、保存重开。

- 四个关键项全部为“✅ 正常”时，可以在矩阵中记录为“关键项正常”；
- 任一关键项为“❌ 有问题”时，记录为“有问题”，并保留 Issue 链接；
- 目录、成稿 / 打印版式、导航窗格和快捷键属于补充项；
- 单独的快捷键冲突不等于模板结构不兼容，因为它可能被系统、输入法、插件或用户自定义设置占用。

### 处理轻量正常反馈

轻量反馈只证明“这个用户实际用过，目前没发现明显问题”。它应单独计数，不能转换成完整验证，也不能用来声称“某版本完全兼容”。

### 用 ChatGPT 维护矩阵

收到新反馈后，可以直接让 ChatGPT：

1. 查找标题以 `[Word 验证]`、`[Word 正常]` 或 `[Word 兼容性]` 开头的新 Issue；
2. 提取操作系统、Word 版本、编号方案、起步版本和关键结果；
3. 对结构版额外记录成稿 / 打印版式测试结果（若用户测试）；
4. 更新 `docs/兼容性验证记录.md`；
5. 保留原 Issue 链接，确保每个结论都能回溯到公开证据。

普通用户不需要参与任何汇总工作。

## 记录原则

维护真实 Word 反馈时：

1. 不要求用户提供个人信息或真实写作内容；
2. 只记录公开 Issue 中明确提供的信息，不根据猜测补全 Word 版本或环境；
3. 不把轻量反馈写成完整验收；
4. 不把自动结构检查写成 Microsoft Word 真机测试；
5. 不使用“完全兼容所有 Word 版本”之类无法证明的措辞。

## 快捷键内部逻辑

Word 的逻辑修饰键在 Windows 与 macOS 中分别对应 Ctrl/Alt 与 Command/Option，因此同一组键位定义分别呈现为：

- Windows：`Ctrl + Alt + ...`
- macOS：`Command + Option + ...`

最终仍分开发布两个平台的模板，因为推荐中文字体不同，而且分平台下载对普通用户更清楚。

## Toolbox 集成边界

`SeekerThinker/toolbox` 只负责项目索引和在线模板选择入口；模板源码、Release、Issues、兼容性记录都继续留在这个独立仓库。不要把 24 个二进制模板复制进 Toolbox，以免产生两份发布源。

Toolbox 使用稳定的 `releases/latest` 下载链接和 `main/templates/...` 单模板路径，因此小版本发布后通常无需同步修改；只有产品结构、路径或选择逻辑变化时才需要更新 Toolbox。

## 发布版本

当前版本号写在根目录 `version.txt`。发布新版本时，先更新 `CHANGELOG.md` 与相关说明，再修改 `version.txt` 触发最终构建和 Release。
