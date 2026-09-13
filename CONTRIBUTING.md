# Contributing

感谢你愿意改进这个项目。

可以贡献：修正文档；报告不同 Word 版本下的兼容问题；优化已有样式和编号；改进 Windows / macOS 使用体验；完善自动检查和真实 Word 验收记录。

从 v3.0 起，项目优先保持稳定。涉及模板文件名、目录、Release 资产名、编号体系或普通用户使用方式的改动，请先阅读 [`STABILITY.md`](STABILITY.md)。兼容的小修复欢迎直接提交；会破坏稳定接口的变化不要在 3.x 中悄悄实施。

提交兼容性问题时，请尽量说明操作系统、Word 版本、涉及的模板，以及是否影响目录、页眉页码、题注、脚注 / 参考文献、导航窗格或快捷键。

如果修改模板生成或 OOXML 后处理逻辑，请先运行：

```bash
pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/reference_support.py
python scripts/verify_templates.py
python scripts/compatibility_check.py
python scripts/manuscript_check.py
python scripts/reference_check.py
python scripts/stability_check.py
```

然后确认 **24 个 `.dotx` 模板**都能通过校验。涉及布局的修改还应渲染模板检查页面效果；PR 和主分支 CI 会继续执行跨平台检查与 24 模板 PDF 布局冒烟测试。

不要手工修改 `templates/` 里的成品来代替生成逻辑，也不要把宏、安装程序或运行时依赖加入普通用户下载包。
