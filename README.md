# Word 结构化思考与写作

**让思路有层级，让结构可调整，让想法持续生长。**

这个项目把 Word 作为思维与写作的辅助工具：用真正的标题层级为想法、问题、笔记和材料命名、分组并建立关系，用导航窗格看见整体，随时回到正文记录、检查和重组。模板不会替你思考，但会让思考的结构更容易被看见、检查和调整。

**整理与积累本身就是完整用途；文章、报告和书稿是可以继续发展的方向，不是预设的终点。** 项目优先顺序始终是：**思考 → 结构 → 记录 / 写作 → 排版。**

[English README](README.en.md) · [项目主页](https://seekerthinker.github.io/word-writing-templates/) · [完整使用说明](https://seekerthinker.github.io/word-writing-templates/guide.html)

## 两种开始方式

**[直接在线开始 →](https://seekerthinker.github.io/word-writing-templates/editor.html)**

在浏览器里一边看左侧标题树，一边连续浏览、编辑全文；给标题分层、改名、拆分、合并或移动整节。也可以切换只读页面预览、专注当前章节。正文支持轻量的加粗、斜体、引用和列表，以及真正的表格、脚注。选择文档语言、编号方案和以后使用 Word 的平台，导出保留真实 Heading 1–4、表格与脚注的 `.docx`，再在本地 Word 中继续。

网页草稿默认存放在**当前浏览器本地**，不会上传到项目服务器；它不是云同步服务。请定期使用「备份 JSON」下载可恢复的项目备份，或导出 `.docx` 保存成文稿；换设备、清理浏览器数据或使用隐私模式前尤其如此。JSON 用「导入备份」恢复，`.docx` 用 Word 打开继续；网页编辑器**尚不支持导入任意 Word 文档并无损往返**。页面预览只近似展示纸张形态，最终分页以 Word 为准。完整操作与局限见 [在线编辑器说明](docs/在线编辑器.md)。

**[下载 Word 模板 →](https://seekerthinker.github.io/word-writing-templates/#chooser)**

也可以直接下载与你的 Windows / macOS 对应的 `.dotx`，双击后由 Word 基于模板新建一份文档，原模板保持不变。在 Word 中使用标题 1–4 和导航窗格记录、检查、重排；目录、页码、题注、脚注、参考文献等可选能力已预置，需要时再用。无需 VBA 宏或额外插件。

[下载 Windows 整包](https://github.com/SeekerThinker/word-writing-templates/releases/latest/download/Word-Writing-Templates-Windows.zip) · [下载 macOS 整包](https://github.com/SeekerThinker/word-writing-templates/releases/latest/download/Word-Writing-Templates-macOS.zip)

## 模板矩阵与编号

v4 坚持**一个编号方案对应一个用户模板**：6 种编号 × Windows / macOS = **12 个 `.dotx`**。界面语言、文档语言和编号方案是不同的选择；英文界面的“Chinese traditional chapter numbering”指中文章节编号，**不是繁体中文语言设置**。

| 类型 | 编号方案 | 示例 | Windows | macOS |
|---|---|---|---|---|
| 书籍 | 中文传统 | `第一章 → 第一节 → 一、 → （一）` | [模板](templates/windows/books/书籍-中文传统.dotx?raw=1) | [模板](templates/macos/books/书籍-中文传统.dotx?raw=1) |
| 书籍 | 章节数字 | `第1章 → 1.1 → 1.1.1 → 1.1.1.1` | [模板](templates/windows/books/书籍-章节数字.dotx?raw=1) | [模板](templates/macos/books/书籍-章节数字.dotx?raw=1) |
| 书籍 | 纯数字 | `1 → 1.1 → 1.1.1 → 1.1.1.1` | [模板](templates/windows/books/书籍-纯数字.dotx?raw=1) | [模板](templates/macos/books/书籍-纯数字.dotx?raw=1) |
| 文章 | 中文论文 | `一、 → （一） → 1. → （1）` | [模板](templates/windows/articles/文章-中文论文.dotx?raw=1) | [模板](templates/macos/articles/文章-中文论文.dotx?raw=1) |
| 文章 | 数字层级 | `1 → 1.1 → 1.1.1 → 1.1.1.1` | [模板](templates/windows/articles/文章-数字层级.dotx?raw=1) | [模板](templates/macos/articles/文章-数字层级.dotx?raw=1) |
| 文章 | 中文简洁 | `一、 → 1. → （1） → ①` | [模板](templates/windows/articles/文章-中文简洁.dotx?raw=1) | [模板](templates/macos/articles/文章-中文简洁.dotx?raw=1) |

日常笔记和材料整理通常可以从「文章 / 日常整理」开始；较长的书稿可看「书籍 / 长篇」。不必一开始就决定最终写成什么。

## 在结构与正文之间来回

把内容放进标题层级，是在不断回答：这一部分究竟讲什么？它属于哪个主题？哪些内容并列、哪些从属？哪里遗漏或重复？顺序是否自然？

先写一点，再用标题命名、归类；看一次导航结构，调整一个位置，再回到正文继续。结构不必预先设计完整，也不必为了最终成稿而存在。[结构化思考方法](docs/结构化思考.md) · [第一次使用 Word 模板](docs/快速开始.md)

## 网页与 Word 的样式快捷键

在网页编辑器和导出的 Word 模板里，标题、正文、引用、表格与脚注沿用同一组快捷键；网页独有的新增章节、移动、备份、导出等操作另有快捷键，见编辑器内的「快捷键」面板。

| 操作 | Windows | macOS |
|---|---|---|
| 标题 1 / 2 / 3 / 4 | `Ctrl + Alt + 1 / 2 / 3 / 4` | `⌘ + ⌥ + 1 / 2 / 3 / 4` |
| 正文 | `Ctrl + Alt + Z` | `⌘ + ⌥ + Z` |
| 表格 / 表格文字 | `Ctrl + Alt + B` | `⌘ + ⌥ + B` |
| 引用 / 特殊段落 | `Ctrl + Alt + Q` | `⌘ + ⌥ + Q` |
| 插入脚注 | `Ctrl + Alt + F` | `⌘ + ⌥ + F` |

## 兼容性与维护

自动化检查 12 个公共模板的 OOXML、编号、样式、分节和可选成稿组件，也检查网页导出包里的真实表格、脚注和快捷键自定义。构建中的 PDF 布局冒烟测试与 OOXML 检查**并不等于**在真实 Microsoft Word 中逐项验收。平台与版本差异见 [兼容性与测试](docs/兼容性与测试.md)。

模板文件名、12 模板矩阵、稳定下载地址及无宏体验由 [STABILITY.md](STABILITY.md) 保护；维护方式见 [MAINTAINERS.md](MAINTAINERS.md)，贡献和测试见 [CONTRIBUTING.md](CONTRIBUTING.md)，AI 协作约定见 [AGENTS.md](AGENTS.md)。项目采用 [MIT License](LICENSE)。

**让标题层级承载思考，让整体始终可见；内容可以停在整理与积累，也可以沿着同一套结构继续发展。**
