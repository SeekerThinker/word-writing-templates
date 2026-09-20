.PHONY: ppf-check web-build web-verify web-publish-check

ppf-check:
	python3 scripts/ppf_contract_check.py

web-build:
	python3 scripts/ppf_build_web.py

web-verify:
	python3 scripts/verify_web_output.py _site

web-publish-check: ppf-check web-build web-verify
