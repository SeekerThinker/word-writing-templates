# Contributing

感谢你愿意改进这个项目。

可以贡献：修正文档；报告不同 Word 版本下的兼容问题；优化样式和编号；建议新的常用编号方案；完善 Windows / macOS 使用体验。

提交修改时，请尽量说明你使用的操作系统、Word 版本、涉及的模板，以及是否影响目录、导航窗格、脚注或表格。

如果修改模板生成逻辑，请先运行：

```bash
pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/verify_templates.py
python scripts/make_quickstart.py
```

然后确认 12 个 `.dotx` 模板都能通过校验。
