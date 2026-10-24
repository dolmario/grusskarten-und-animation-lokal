"""3e: Foto -> Video mit LTX-2.5 (distilled / dev) ueber die umgesetzte Vorlage video_ltx2_5_i2v.

python ltx_lauf.py --server http://127.0.0.1:8188 --ziel R\\video --quelle eigene \
    --bilder R\\kolorieren\\qwen2511edit\\01-hochzeit-warten-1907_seed11.png ... --modelle distilled dev --seed 11
Je Lauf: MP4 nach <ziel>\\<Modellname>\\, API-Prompt als .api.json daneben, Zeiten in <ziel>\\messungen.jsonl
(Start- und Endzeit erlauben es, VRAM-/RAM-Spitzen aus nvidia-smi.csv und ram-comfyui.csv abzulesen).
"""
import argparse, json, mimetypes, time, urllib.parse, urllib.request, uuid
from pathlib import Path

import ltx_api

MODELLE = {
    'distilled': ('ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors', 'LTX-2.5 distilled'),
    'dev': ('ltx-2.5-22b-dev-transformer-comfy-int8-convrot.safetensors', 'LTX-2.5 dev'),
}
PROMPTS = Path(__file__).resolve().parent.parent / 'prompts'


def hochladen(server, pfad: Path) -> str:
    grenze = uuid.uuid4().hex
    daten = pfad.read_bytes()
    typ = mimetypes.guess_type(pfad.name)[0] or 'image/png'
    koerper = (f'--{grenze}\r\nContent-Disposition: form-data; name="image"; filename="{pfad.name}"\r\nContent-Type: {typ}\r\n\r\n').encode() \
        + daten + f'\r\n--{grenze}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n--{grenze}--\r\n'.encode()
    anfrage = urllib.request.Request(server + '/upload/image', data=koerper, headers={'Content-Type': f'multipart/form-data; boundary={grenze}'})
    with urllib.request.urlopen(anfrage) as r:
        return json.load(r)['name']


def senden(server, pfad, daten=None):
    kopf = {'Content-Type': 'application/json'}
    anfrage = urllib.request.Request(server + pfad, data=json.dumps(daten).encode() if daten is not None else None, headers=kopf)
    with urllib.request.urlopen(anfrage, timeout=600) as r:
        return json.load(r)


def main():
    z = argparse.ArgumentParser()
    z.add_argument('--server', default='http://127.0.0.1:8188')
    z.add_argument('--ziel', required=True)
    z.add_argument('--quelle', required=True, help='eigene oder evo (nur fuer den Dateinamen)')
    z.add_argument('--bilder', nargs='+', required=True)
    z.add_argument('--modelle', nargs='+', default=['distilled', 'dev'], choices=sorted(MODELLE))
    z.add_argument('--prompts', nargs='+', default=['kurz', 'lang'])
    z.add_argument('--seed', type=int, default=11)
    z.add_argument('--limit-min', type=int, default=90)
    z.add_argument('--aspect', default=None, help='z. B. "3:4 (Portrait Standard)"; ohne Angabe Vorlagenwert')
    z.add_argument('--megapixel', type=float, default=None)
    a = z.parse_args()
    server = a.server.rstrip('/')
    ziel = Path(a.ziel)
    for m in a.modelle:
        unet, lesbar = MODELLE[m]
        for bild in map(Path, a.bilder):
            hoch = hochladen(server, bild)
            for pk in a.prompts:
                text = (PROMPTS / f'bewegung-{pk}.txt').read_text(encoding='utf-8').strip()
                kurz = bild.stem.split('_seed')[0]
                name = f'{lesbar} - {a.quelle} - {kurz} - {pk} - seed{a.seed}'
                datei = ziel / lesbar / (name + '.mp4')
                if datei.exists():
                    continue
                try:
                    ablauf = ltx_api.baue(server, hoch, text, unet, a.seed, praefix=f'ltx_{m}_{a.quelle}_{kurz}_{pk}', aspect=a.aspect, megapixel=a.megapixel)
                except Exception as e:
                    print('UMSETZUNG FEHLGESCHLAGEN', repr(e), flush=True); raise
                begonnen, t0 = time.strftime('%Y-%m-%dT%H:%M:%S'), time.time()
                fehler = None
                eintrag = {}
                try:
                    auftrag = senden(server, '/prompt', {'prompt': ablauf})['prompt_id']
                    while time.time() - t0 < a.limit_min * 60:
                        verlauf = senden(server, f'/history/{auftrag}')
                        if auftrag in verlauf and verlauf[auftrag].get('status', {}).get('completed') is not None:
                            eintrag = verlauf[auftrag]
                            break
                        time.sleep(3)
                    else:
                        senden(server, '/interrupt', {})
                        fehler = f'Zeitlimit {a.limit_min} min'
                except urllib.error.HTTPError as e:
                    fehler = 'HTTP %s: %s' % (e.code, e.read().decode('utf-8', 'replace')[:2000])
                except Exception as e:
                    fehler = repr(e)
                ok = eintrag.get('status', {}).get('status_str') == 'success'
                if ok:
                    for k in eintrag.get('outputs', {}).values():
                        for b in k.get('images', []):
                            q = f'{server}/view?filename={urllib.parse.quote(b["filename"])}&subfolder={urllib.parse.quote(b.get("subfolder", ""))}&type={b.get("type", "output")}'
                            datei.parent.mkdir(parents=True, exist_ok=True)
                            with urllib.request.urlopen(q, timeout=600) as r:
                                datei.write_bytes(r.read())
                elif not fehler:
                    fehler = json.dumps(eintrag.get('status', {}), ensure_ascii=False)[:2000]
                datei.parent.mkdir(parents=True, exist_ok=True)
                datei.with_suffix('.api.json').write_text(json.dumps({'prompt': ablauf, 'history': eintrag}, ensure_ascii=False, indent=1), encoding='utf-8')
                erg = {'modell': lesbar, 'quelle': a.quelle, 'bild': kurz, 'prompt': pk, 'seed': a.seed, 'start': begonnen,
                       'ende': time.strftime('%Y-%m-%dT%H:%M:%S'), 'gesamt_s': round(time.time() - t0, 1), 'ok': ok and datei.exists(), 'fehler': fehler,
                       'datei': datei.name if datei.exists() else None}
                ziel.mkdir(parents=True, exist_ok=True)
                with (ziel / 'messungen.jsonl').open('a', encoding='utf-8') as f:
                    f.write(json.dumps(erg, ensure_ascii=False) + '\n')
                print(json.dumps(erg, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
