"""Schwarz-Weiß-Fotos lokal kolorieren mit Qwen-Image-Edit 2511 (Apache 2.0) oder Qwen-Image 2.1 (Forschungslizenz).

Aufruf:
    python kolorieren.py qwen2511edit qwen21edit --bilder a.jpg b.jpg --seeds 11,22
    python kolorieren.py qwen2511edit --server http://127.0.0.1:8188 --ziel E:\\rueckgabe\\kolorieren --bilder ...
Ohne --server startet das Skript ComfyUI-qwen selbst (stapel.py nötig) und beendet es danach.
"""
import argparse, json, threading, time, urllib.parse, urllib.request, uuid
from pathlib import Path

HIER = Path(__file__).resolve().parent
ZIEL = Path('ergebnisse')
PROMPT = ('Colorize this black-and-white photograph with natural, restrained colors. Preserve facial identity, age, expression, '
          'pose, clothing details, background and framing. Add color only.')


def qwen21edit(bild, seed, name):
    return {
        '1': {'class_type': 'UNETLoader', 'inputs': {'unet_name': 'qwen_image_2.1_int8_convrot.safetensors', 'weight_dtype': 'default'}},
        '2': {'class_type': 'CLIPLoader', 'inputs': {'clip_name': 'qwen3vl_8b_int8_convrot.safetensors', 'type': 'qwen_image', 'device': 'default'}},
        '3': {'class_type': 'VAELoader', 'inputs': {'vae_name': 'qwen_image_2.1_vae_bf16.safetensors'}},
        '8': {'class_type': 'LoadImage', 'inputs': {'image': bild}},
        '4': {'class_type': 'TextEncodeQwenImage21', 'inputs': {'clip': ['2', 0], 'vae': ['3', 0], 'prompt': PROMPT, 'negative_prompt': '',
                                                               'resolution': 1024, 'images.image_1': ['8', 0]}},
        '5': {'class_type': 'KSampler', 'inputs': {'model': ['1', 0], 'seed': seed, 'steps': 25, 'cfg': 1.0, 'sampler_name': 'euler',
                                                   'scheduler': 'simple', 'positive': ['4', 0], 'negative': ['4', 1],
                                                   'latent_image': ['4', 2], 'denoise': 1.0}},
        '6': {'class_type': 'VAEDecode', 'inputs': {'samples': ['5', 0], 'vae': ['3', 0]}},
        '7': {'class_type': 'SaveImage', 'inputs': {'images': ['6', 0], 'filename_prefix': name}},
    }, 25


def qwen2511edit(bild, seed, name):
    # Aufbau und Werte nach der ComfyUI-Vorlage für Qwen-Image-Edit 2511: 40 Schritte, CFG 4, AuraFlow 3,1, CFGNorm.
    return {
        '1': {'class_type': 'UNETLoader', 'inputs': {'unet_name': 'qwen_image_edit_2511_int8_convrot.safetensors', 'weight_dtype': 'default'}},
        '2': {'class_type': 'CLIPLoader', 'inputs': {'clip_name': 'qwen_2.5_vl_7b_fp8_scaled.safetensors', 'type': 'qwen_image', 'device': 'default'}},
        '3': {'class_type': 'VAELoader', 'inputs': {'vae_name': 'qwen_image_vae.safetensors'}},
        '4': {'class_type': 'LoadImage', 'inputs': {'image': bild}},
        '5': {'class_type': 'FluxKontextImageScale', 'inputs': {'image': ['4', 0]}},
        '6': {'class_type': 'TextEncodeQwenImageEditPlus', 'inputs': {'clip': ['2', 0], 'prompt': PROMPT, 'vae': ['3', 0], 'image1': ['5', 0]}},
        '7': {'class_type': 'TextEncodeQwenImageEditPlus', 'inputs': {'clip': ['2', 0], 'prompt': '', 'vae': ['3', 0], 'image1': ['5', 0]}},
        '8': {'class_type': 'FluxKontextMultiReferenceLatentMethod', 'inputs': {'conditioning': ['6', 0], 'reference_latents_method': 'index_timestep_zero'}},
        '9': {'class_type': 'FluxKontextMultiReferenceLatentMethod', 'inputs': {'conditioning': ['7', 0], 'reference_latents_method': 'index_timestep_zero'}},
        '10': {'class_type': 'ModelSamplingAuraFlow', 'inputs': {'model': ['1', 0], 'shift': 3.1}},
        '11': {'class_type': 'CFGNorm', 'inputs': {'model': ['10', 0], 'strength': 1.0}},
        '12': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['5', 0], 'vae': ['3', 0]}},
        '13': {'class_type': 'KSampler', 'inputs': {'model': ['11', 0], 'seed': seed, 'steps': 40, 'cfg': 4.0, 'sampler_name': 'euler',
                                                    'scheduler': 'simple', 'positive': ['8', 0], 'negative': ['9', 0],
                                                    'latent_image': ['12', 0], 'denoise': 1.0}},
        '14': {'class_type': 'VAEDecode', 'inputs': {'samples': ['13', 0], 'vae': ['3', 0]}},
        '15': {'class_type': 'SaveImage', 'inputs': {'images': ['14', 0], 'filename_prefix': name}},
    }, 40


def _flux2_edit(bild, seed, name, unet, clip, steps, gguf=False, guidance=None):
    lader = ({'class_type': 'UnetLoaderGGUF', 'inputs': {'unet_name': unet}} if gguf else
             {'class_type': 'UNETLoader', 'inputs': {'unet_name': unet, 'weight_dtype': 'default'}})
    ablauf = {
        '1': lader,
        '2': {'class_type': 'CLIPLoader', 'inputs': {'clip_name': clip, 'type': 'flux2', 'device': 'default'}},
        '3': {'class_type': 'VAELoader', 'inputs': {'vae_name': 'flux2-vae.safetensors'}},
        '4': {'class_type': 'LoadImage', 'inputs': {'image': bild}},
        '5': {'class_type': 'ImageScaleToTotalPixels', 'inputs': {'image': ['4', 0], 'upscale_method': 'lanczos', 'megapixels': 1.0, 'resolution_steps': 32}},
        '6': {'class_type': 'GetImageSize', 'inputs': {'image': ['5', 0]}},
        '7': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['5', 0], 'vae': ['3', 0]}},
        '8': {'class_type': 'CLIPTextEncode', 'inputs': {'text': PROMPT, 'clip': ['2', 0]}},
        '10': {'class_type': 'ReferenceLatent', 'inputs': {'conditioning': ['8', 0], 'latent': ['7', 0]}},
        '13': {'class_type': 'Flux2Scheduler', 'inputs': {'steps': steps, 'width': ['6', 0], 'height': ['6', 1]}},
        '14': {'class_type': 'EmptyFlux2LatentImage', 'inputs': {'width': ['6', 0], 'height': ['6', 1], 'batch_size': 1}},
        '15': {'class_type': 'RandomNoise', 'inputs': {'noise_seed': seed}},
        '16': {'class_type': 'KSamplerSelect', 'inputs': {'sampler_name': 'euler'}},
        '17': {'class_type': 'SamplerCustomAdvanced', 'inputs': {'noise': ['15', 0], 'guider': ['12', 0], 'sampler': ['16', 0],
                                                                  'sigmas': ['13', 0], 'latent_image': ['14', 0]}},
        '18': {'class_type': 'VAEDecode', 'inputs': {'samples': ['17', 0], 'vae': ['3', 0]}},
        '19': {'class_type': 'SaveImage', 'inputs': {'images': ['18', 0], 'filename_prefix': name}},
    }
    if guidance:
        # FLUX.2 dev: Führung eingebacken, wie in bildvergleich.py.
        ablauf['9'] = {'class_type': 'FluxGuidance', 'inputs': {'conditioning': ['10', 0], 'guidance': guidance}}
        ablauf['12'] = {'class_type': 'BasicGuider', 'inputs': {'model': ['1', 0], 'conditioning': ['9', 0]}}
    else:
        ablauf['9'] = {'class_type': 'ConditioningZeroOut', 'inputs': {'conditioning': ['8', 0]}}
        ablauf['11'] = {'class_type': 'ReferenceLatent', 'inputs': {'conditioning': ['9', 0], 'latent': ['7', 0]}}
        ablauf['12'] = {'class_type': 'CFGGuider', 'inputs': {'model': ['1', 0], 'positive': ['10', 0], 'negative': ['11', 0], 'cfg': 1.0}}
    return ablauf, steps


def klein4edit(bild, seed, name):
    return _flux2_edit(bild, seed, name, 'flux-2-klein-4b-fp8.safetensors', 'qwen_3_4b.safetensors', 4)


def klein9edit(bild, seed, name):
    return _flux2_edit(bild, seed, name, 'flux-2-klein-9b-fp8.safetensors', 'qwen_3_8b_fp8mixed.safetensors', 4)


def fluxdevedit(bild, seed, name):
    return _flux2_edit(bild, seed, name, 'flux2-dev-Q4_K_M.gguf', 'mistral_3_small_flux2_fp4_mixed.safetensors', 20, gguf=True, guidance=4.0)


ABLAEUFE = {'qwen21edit': qwen21edit, 'qwen2511edit': qwen2511edit, 'klein4edit': klein4edit, 'klein9edit': klein9edit,
            'fluxdevedit': fluxdevedit}
# Ohne --server: FLUX.2 dev läuft in der Original-Installation (GGUF-Knoten), alles andere in ComfyUI-qwen.
INSTANZ_SCHLUESSEL = {'fluxdevedit': 'flux'}


def senden(server, pfad, nutzlast=None):
    daten = json.dumps(nutzlast).encode() if nutzlast is not None else None
    anfrage = urllib.request.Request(server + pfad, data=daten, headers={'Content-Type': 'application/json'} if daten else {})
    with urllib.request.urlopen(anfrage, timeout=600) as antwort:
        return json.loads(antwort.read())


def hochladen(server, pfad):
    grenze = uuid.uuid4().hex
    kopf = (f'--{grenze}\r\nContent-Disposition: form-data; name="image"; filename="{pfad.name}"\r\n'
            'Content-Type: application/octet-stream\r\n\r\n').encode()
    rumpf = kopf + pfad.read_bytes() + f'\r\n--{grenze}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n--{grenze}--\r\n'.encode()
    anfrage = urllib.request.Request(server + '/upload/image', data=rumpf, headers={'Content-Type': f'multipart/form-data; boundary={grenze}'})
    with urllib.request.urlopen(anfrage, timeout=120) as antwort:
        return json.loads(antwort.read())['name']


class Speicher(threading.Thread):
    """Spitzenwert der Grafik-Speicherzähler von Windows (Dedicated + Shared, bei NVIDIA zusätzlich nvidia-smi mitschreiben)."""
    def __init__(self):
        super().__init__(daemon=True); self.werte = []; self.halt = False

    def run(self):
        import subprocess
        befehl = ("(Get-Counter '\\GPU Adapter Memory(*)\\Shared Usage','\\GPU Adapter Memory(*)\\Dedicated Usage').CounterSamples | "
                  "Measure-Object CookedValue -Sum | ForEach-Object { [math]::Round($_.Sum/1GB,2) }")
        while not self.halt:
            aus = subprocess.run(['powershell.exe', '-NoProfile', '-Command', befehl], capture_output=True, text=True).stdout.strip()
            try: self.werte.append(float(aus.replace(',', '.')))
            except ValueError: pass
            time.sleep(2)


def lauf(server, ziel, modell, bild, seed):
    hochgeladen = hochladen(server, bild)
    name = f'kolor_{modell}_{bild.stem}_{seed}'
    ablauf, schritte = ABLAEUFE[modell](hochgeladen, seed, name)
    speicher = Speicher(); speicher.start()
    begonnen = time.time()
    auftrag = senden(server, '/prompt', {'prompt': ablauf})['prompt_id']
    while True:
        verlauf = senden(server, f'/history/{auftrag}')
        if auftrag in verlauf and verlauf[auftrag].get('status', {}).get('completed') is not None:
            break
        time.sleep(2)
    speicher.halt = True; speicher.join()
    eintrag = verlauf[auftrag]
    bilder = [b['filename'] for k in eintrag.get('outputs', {}).values() for b in k.get('images', [])]
    ordner = ziel / modell
    ordner.mkdir(parents=True, exist_ok=True)
    datei = ordner / f'{bild.stem}_seed{seed}.png'
    for b in bilder:
        with urllib.request.urlopen(f'{server}/view?filename={urllib.parse.quote(b)}&type=output', timeout=120) as antwort:
            datei.write_bytes(antwort.read())
    datei.with_suffix('.api.json').write_text(json.dumps({'prompt': ablauf, 'history': eintrag}, ensure_ascii=False, indent=1), encoding='utf-8')
    ergebnis = {'modell': modell, 'bild': bild.name, 'seed': seed, 'schritte': schritte, 'gesamt_s': round(time.time() - begonnen, 1),
                'speicher_max_gb': max(speicher.werte) if speicher.werte else None,
                'ok': eintrag.get('status', {}).get('status_str') == 'success', 'zeit': time.strftime('%Y-%m-%d %H:%M:%S')}
    with (ziel / 'messungen.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(ergebnis, ensure_ascii=False) + '\n')
    print(json.dumps(ergebnis, ensure_ascii=False), flush=True)


def main():
    z = argparse.ArgumentParser()
    z.add_argument('modelle', nargs='+', choices=sorted(ABLAEUFE))
    z.add_argument('--bilder', nargs='+', required=True)
    z.add_argument('--seeds', default='11,22')
    z.add_argument('--ziel', default=str(ZIEL))
    z.add_argument('--prompt', default='', help='anderer Bearbeitungsauftrag statt Kolorieren, z. B. Kleidung tauschen')
    z.add_argument('--server', default='', help='laufendes ComfyUI, z. B. http://127.0.0.1:8188; dann wird kein Server gestartet')
    a = z.parse_args()
    global PROMPT
    if a.prompt:
        PROMPT = a.prompt
    ziel = Path(a.ziel); ziel.mkdir(parents=True, exist_ok=True)
    bilder = [Path(b) for b in a.bilder]
    for b in bilder:
        if not b.exists():
            raise SystemExit(f'Bild fehlt: {b}')
    seeds = [int(s) for s in a.seeds.split(',')]
    for modell in a.modelle:
        proc = None
        if a.server:
            server = a.server.rstrip('/')
        else:
            import stapel
            ordner, venv, port = stapel.INSTANZ[INSTANZ_SCHLUESSEL.get(modell, 'qwen')]
            proc, server = stapel.server_start(ordner, venv, port), f'http://127.0.0.1:{port}'
        try:
            for b in bilder:
                for s in seeds:
                    if (ziel / modell / f'{b.stem}_seed{s}.png').exists():
                        continue
                    lauf(server, ziel, modell, b, s)
        finally:
            if proc:
                stapel.server_stop(proc)


if __name__ == '__main__':
    main()
