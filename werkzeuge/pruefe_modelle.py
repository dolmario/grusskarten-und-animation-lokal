"""Read-only installed-model checker. No installs, downloads or server changes."""
from pathlib import Path
import json, hashlib, sys
if len(sys.argv)!=2: sys.exit('Usage: python pruefe_modelle.py PATH_TO_COMFYUI')
root=Path(sys.argv[1]).resolve()
manifest=Path(__file__).resolve().parents[1]/'installation/MODELS.json'
fail=False
for m in json.loads(manifest.read_text(encoding='utf-8')):
    p=root/m['path']
    if not p.is_file(): print('MISSING',m['scope'],m['path']); fail=True; continue
    if m['bytes'] and p.stat().st_size!=m['bytes']: print('SIZE MISMATCH',m['path']); fail=True; continue
    if m['sha256']:
        h=hashlib.sha256()
        with p.open('rb') as f:
            for block in iter(lambda:f.read(8*1024*1024),b''): h.update(block)
        ok=h.hexdigest()==m['sha256'];print('HASH OK' if ok else 'HASH MISMATCH',m['path']);fail|=not ok
    else: print('EXISTS; HASH UNKNOWN',m['path'])
sys.exit(1 if fail else 0)
