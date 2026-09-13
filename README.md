# Word 结构化写作模板集

**不用配置 Word：下载 → 选模板 → 双击 → 开始写。**

这是一个面向普通 Word 用户的中文结构化写作模板库。你不需要懂 GitHub、VBA、多级列表或 Word 样式设置；成品模板已经预置好标题层级、自动编号、正文样式和快捷键。

> 支持 Microsoft Word for Windows 与 Microsoft Word for macOS。两个平台分别提供成品模板，以减少字体和快捷键差异带来的问题。

## 一键下载

- **Windows：** [下载 Windows 模板包](release/Word结构化写作模板-Windows-v2.0.0.zip?raw=1)
- **MacBook / macOS：** [下载 macOS 模板包](release/Word结构化写作模板-macOS-v2.0.0.zip?raw=1)
- 也可以到 [Releases](../../releases/latest) 下载最新版。

下载 ZIP 后解压，先看 `00-开始使用.pdf`，或者直接进入“书籍模板 / 文章模板”，**双击 `.dotx` 文件**。Word 会基于模板新建文档，原模板不会被改坏。

## 选哪个模板？

### 📚 写书

| 模板 | 标题编号效果 | 适合 |
|---|---|---|
| 中文传统 | `第一章 → 第一节 → 一、 → （一）` | 中文专著、教材、长篇作品 |
| 章节数字 | `第1章 → 1.1 → 1.1.1 → 1.1.1.1` | 技术书、教程、研究专著 |
| 纯数字 | `1 → 1.1 → 1.1.1 → 1.1.1.1` | 现代简洁型长文、电子书 |

### 📄 写文章

| 模板 | 标题编号效果 | 适合 |
|---|---|---|
| 中文论文 | `一、 → （一） → 1. → （1）` | 中文论文、报告、正式文章 |
| 数字层级 | `1 → 1.1 → 1.1.1 → 1.1.1.1` | 学术、研究、技术文章 |
| 中文简洁 | `一、 → 1. → （1） → ①` | 长文章、随笔、内容写作 |

## 快捷键

所有模板都内置四级标题、正文、表格文字、引用和脚注快捷键。

| 用途 | Windows | macOS |
|---|---|---|
| 一级标题 | `Ctrl + Alt + 1` | `⌘ + ⌥ + 1` |
| 二级标题 | `Ctrl + Alt + 2` | `⌘ + ⌥ + 2` |
| 三级标题 | `Ctrl + Alt + 3` | `⌘ + ⌥ + 3` |
| 四级标题 | `Ctrl + Alt + 4` | `⌘ + ⌥ + 4` |
| 正文 | `Ctrl + Alt + Z` | `⌘ + ⌥ + Z` |
| 表格文字 | `Ctrl + Alt + B` | `⌘ + ⌥ + B` |
| 引用 / 特别内容 | `Ctrl + Alt + Q` | `⌘ + ⌥ + Q` |
| 插入脚注 | `Ctrl + Alt + F` | `⌘ + ⌥ + F` |

不会快捷键也没关系：可以直接从 Word 的“样式”区域选择标题和正文样式。

## 为什么使用 `.dotx`？

`.dotx` 是 Word 的模板格式。双击它时，Word 会创建一个新的文档，而不是让你直接修改模板本身。因此不需要“先复制一份模板再删除示例内容”。

模板打开后只有非常少的占位内容：标题、一级标题和第一段正文。直接把它们改成自己的内容即可。

## 能做什么？

- 四级标题自动编号
- 自动生成 / 更新目录
- 使用 Word 导航窗格查看全文结构
- 在导航窗格中拖动标题，整体移动章节
- 长文档多窗口对照编辑
- 大纲视图与 Web 版式辅助长文写作
- Windows 与 macOS 分平台优化字体与快捷键

详细说明见 [`docs/`](docs/)。

## 给维护者

普通用户不需要阅读这一节。仓库中的模板和下载包由脚本自动生成；维护时只修改脚本和文档，然后由 GitHub Actions 重新生成 12 个成品模板与两个用户下载包。

```text
word-writing-templates/
├── templates/             # 自动生成：12 个 .dotx 成品模板
├── release/               # 自动生成：Windows / macOS 用户 ZIP
├── docs/                  # 普通用户说明
├── scripts/               # 模板生成、校验、打包
├── .github/workflows/     # 自动构建与发布
└── toolbox/               # 接入 SeekerThinker/toolbox 的索引片段
```

本地生成：

```bash
pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/verify_templates.py
python scripts/make_quickstart.py
python scripts/build_release.py
```

## 开源许可

MIT License。见 [`LICENSE`](LICENSE)。
