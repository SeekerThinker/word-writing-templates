from pathlib import Path
required=['project-stack.yaml','project-stack.lock.yaml','AHICP_MANIFEST.yaml','AHICP_CONTEXT_INTERFACE.yaml','PPF_MANIFEST.yaml','VAULT_INTERFACE_MANIFEST.yaml','publishing.yaml','cloudflare-builds.yaml','docs/continuous-web/ACCESS-POLICY.md','project.yaml','website.yaml']
missing=[p for p in required if not Path(p).exists()]
if missing: raise SystemExit('Missing required stack files: '+', '.join(missing))
pub=Path('publishing.yaml').read_text(encoding='utf-8')
for token in ['schema: ppf/v0.1','mode: continuous','authorization_state: authorized','visibility: public','canonical_publish_gate: make web-publish-check','enabled: false']:
    if token not in pub: raise SystemExit(f'publishing.yaml missing: {token}')
print('PPF/AHICP structural contract: OK')
