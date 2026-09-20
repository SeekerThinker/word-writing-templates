from pathlib import Path
import sys
root=Path(sys.argv[1]); index=root/'index.html'
if not index.is_file(): raise SystemExit(f'Web output index missing: {index}')
print(f'Web output verified: {index}')
