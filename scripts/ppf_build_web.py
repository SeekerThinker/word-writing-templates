from pathlib import Path
import shutil
site=Path('site'); out=Path('_site')
if out.exists(): shutil.rmtree(out)
shutil.copytree(site,out)
previews=out/'previews'; previews.mkdir(parents=True,exist_ok=True)
for source in Path('docs/assets/previews').glob('*.png'): shutil.copy2(source,previews/source.name)
shutil.copytree(Path('templates'),out/'templates')
for name in ['index.html','guide.html']:
    p=out/name; text=p.read_text(encoding='utf-8')
    marker='<script src="./app.js"></script>' if name=='index.html' else '</body>'
    inject='<script src="./i18n.js"></script>\n  <script src="./app.js"></script>' if name=='index.html' else '  <script src="./i18n.js"></script>\n</body>'
    if marker in text: p.write_text(text.replace(marker,inject),encoding='utf-8')
(out/'.nojekyll').touch()
print('PPF web output assembled at _site')
