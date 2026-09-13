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
python scripts/make_quickstart.py
```

GitHub Actions 会在 `main` 的维护文件发生变化后自动执行生成、校验、打包，并更新 GitHub Release。

## 快捷键内部逻辑

Word 的逻辑修饰键在 Windows 与 macOS 中分别对应 Ctrl/Alt 与 Command/Option，因此同一组键位定义分别呈现为：

- Windows：`Ctrl + Alt + ...`
- macOS：`Command + Option + ...`

最终仍分开发布两个平台的模板，因为推荐中文字体不同，而且分平台下载对普通用户更清楚。

## 发布版本

当前版本号写在根目录 `version.txt`。发布新版本时，先修改该文件，再更新 `CHANGELOG.md`。
