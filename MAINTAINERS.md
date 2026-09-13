# 维护者说明

这个项目的原则是：**普通用户零配置；复杂性留在维护端。**

## 发布矩阵

6 种结构 × 2 个平台 = 12 个最终 `.dotx` 模板。

- 书籍：中文传统 / 章节数字 / 纯数字
- 文章：中文论文 / 数字层级 / 中文简洁
- 平台：Windows / macOS

## 生成方式

模板由 `python-docx + OOXML` 从代码生成。修改字体、编号、快捷键或占位内容时，只需要修改生成逻辑，再统一生成全部成品。

```bash
pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/verify_templates.py
python scripts/compatibility_check.py
python scripts/make_quickstart.py
```

GitHub Actions 会在 `main` 的维护文件发生变化后自动执行生成、校验、打包，并更新 GitHub Release。

## 跨平台检查

`compatibility_check.py` 只使用 Python 标准库，因此会在 GitHub Actions 的 Windows、macOS 与 Linux runner 上运行同一套检查，主要覆盖：

- `.dotx` OOXML 包结构与中文路径；
- 四级标题编号；
- Windows / macOS 平台字体；
- 快捷键映射；
- 宏文件缺失检查。

这属于**结构兼容性检查**，不会启动 Microsoft Word。不要在文档或 Release 说明中把它描述成“所有版本 Word 真机测试通过”。真实 Word 版本、输入法、插件和系统快捷键冲突仍应通过实际使用反馈补充验证。

## 真实 Word 验证记录

v2.4.0 起使用三件东西收集真实环境证据：

- `docs/真实Word验收.md`：面向普通用户的 3～5 分钟测试步骤；
- `.github/ISSUE_TEMPLATE/word_compatibility_report.md`：统一收集系统、Word 版本、模板和测试结果；
- `docs/兼容性验证记录.md`：只登记公开、可追踪的真实 Word 结果。

维护者处理兼容性 Issue 时遵循下面的规则：

1. 不要求用户提供个人信息或真实写作内容；
2. 至少记录操作系统、Word 版本、模板名称、能否由 `.dotx` 新建文档、四级标题编号是否正常、保存再打开是否正常；
3. 目录、导航窗格和快捷键属于补充验证项；
4. 单独的快捷键冲突不等于模板结构不兼容，因为快捷键可能被系统、输入法、插件或用户自定义占用；
5. 只有存在公开 Issue 作为证据时，才把对应环境加入 `docs/兼容性验证记录.md` 的“已确认”区域；
6. 不使用“完全兼容所有 Word 版本”之类无法证明的措辞。

## 快捷键内部逻辑

Word 的逻辑修饰键在 Windows 与 macOS 中分别对应 Ctrl/Alt 与 Command/Option，因此同一组键位定义分别呈现为：

- Windows：`Ctrl + Alt + ...`
- macOS：`Command + Option + ...`

最终仍分开发布两个平台的模板，因为推荐中文字体不同，而且分平台下载对普通用户更清楚。

## 发布版本

当前版本号写在根目录 `version.txt`。发布新版本时，先更新 `CHANGELOG.md` 与相关说明，再修改 `version.txt` 触发最终构建和 Release。