"""Setzt die ComfyUI-Vorlage video_ltx2_5_i2v (UI-Format mit Subgraph) in ein API-Prompt um.

Brauchbar als Modul: baue(server, bild, prompt, unet, seed) -> API-Prompt-Dict.
Der Subgraph wird aufgeloest (IDs "<instanz>:<knoten>"), Widget-Werte kommen aus der Vorlage,
die Reihenfolge der Widgets aus /object_info des laufenden ComfyUI.
"""
import copy, json, urllib.request
from pathlib import Path

VORLAGE = Path(__file__).with_name('video_ltx2_5_i2v.template.json')
SKIP = {'MarkdownNote', 'Note', 'PreviewAny'}


def _holen(server, pfad):
    with urllib.request.urlopen(server + pfad) as r:
        return json.load(r)


def _linkdict(links):
    d = {}
    for l in links:
        if isinstance(l, dict):
            d[l['id']] = (l['origin_id'], l['origin_slot'], l['target_id'], l['target_slot'])
        else:
            d[l[0]] = (l[1], l[2], l[3], l[4])
    return d


def _widgetnamen(info):
    """Namen der Widget-Eingaben in Reihenfolge, mit Kennzeichen, ob ein control_after_generate-Wert folgt."""
    out = []
    for gruppe in ('required', 'optional'):
        for name, spec in (info.get('input', {}).get(gruppe) or {}).items():
            typ = spec[0]
            opt = spec[1] if len(spec) > 1 and isinstance(spec[1], dict) else {}
            if isinstance(typ, list) or all(t in ('INT', 'FLOAT', 'STRING', 'BOOLEAN', 'COMBO') for t in str(typ).split(',')):
                out.append((name, bool(opt.get('control_after_generate'))))
    return out


def baue(server, bild, prompt, unet, seed, praefix='ltx', vorlage=VORLAGE, aspect=None, megapixel=None):
    oi = _holen(server, '/object_info')
    ui = json.loads(Path(vorlage).read_text(encoding='utf-8'))
    sg = ui['definitions']['subgraphs'][0]
    api = {}

    def knoten_uebernehmen(knoten, links, praefix_id, eingaenge_aufloesen):
        """Alle Knoten einer Ebene in api eintragen."""
        for n in knoten:
            t = n['type']
            if t in SKIP or t not in oi:
                continue
            nid = f'{praefix_id}{n["id"]}'
            info = oi[t]
            werte = list(n.get('widgets_values') or [])
            eing = {}
            verlinkt = set()
            for i in n.get('inputs', []):
                if i.get('link') is not None:
                    quelle = eingaenge_aufloesen(links[i['link']])
                    if quelle is not None:
                        eing[i['name']] = quelle
                        verlinkt.add(i['name'])
            for name, kontrolle in _widgetnamen(info):
                if not werte:
                    break
                v = werte.pop(0)
                if kontrolle and werte:
                    werte.pop(0)
                if name not in verlinkt:
                    eing[name] = v
            api[nid] = {'class_type': t, 'inputs': eing}

    # --- Subgraph-Instanz herausfinden
    inst = next(n for n in ui['nodes'] if n['type'] == sg['id'])
    inst_id = inst['id']
    sg_namen = [i['name'] for i in sg['inputs']]
    wnamen = [n for n in sg_namen if n != 'input']
    wvals = dict(zip(wnamen, inst.get('widgets_values') or []))
    top_links = _linkdict(ui['links'])
    sg_links = _linkdict(sg['links'])

    def top_quelle(l):
        if l[0] == inst_id:   # Ausgang des Subgraphen -> innerer Knoten
            for sl in sg_links.values():
                if sl[2] == -20 and sl[3] == l[1]:
                    return [f'{inst_id}:{sl[0]}', sl[1]]
        return [str(l[0]), l[1]]

    # Subgraph-Eingaenge: Bild/Verbindungen von der oberen Ebene
    inst_eingang = {}
    for i in inst.get('inputs', []):
        if i.get('link') is not None:
            inst_eingang[i['name']] = top_quelle(top_links[i['link']])
    # Widget-Werte ueberschreiben (Prompt, Seed, Modell)
    wvals['value'] = prompt
    wvals['value_1'] = False          # prompt_enhance aus
    wvals['noise_seed'] = seed
    wvals['unet_name'] = unet

    def sg_aufloesen(l):
        origin, slot, _t, _ts = l
        if origin == -10:
            name = sg_namen[slot]
            if name in inst_eingang:
                return inst_eingang[name]
            return ('WERT', wvals.get(name))
        return [f'{inst_id}:{origin}', slot]

    # obere Ebene
    ob = [n for n in ui['nodes'] if n['id'] != inst_id]
    knoten_uebernehmen(ob, top_links, '', top_quelle)
    # Subgraph
    knoten_uebernehmen(sg['nodes'], sg_links, f'{inst_id}:', sg_aufloesen)

    # WERT-Platzhalter in feste Werte umwandeln
    for k in api.values():
        for name, v in list(k['inputs'].items()):
            if isinstance(v, tuple) and v and v[0] == 'WERT':
                k['inputs'][name] = v[1]

    # Sonderfaelle: ResizeImageMaskNode (dynamisches Combo, Werte aus der Vorlage: scale longer dimension | 1536 | lanczos)
    # und Prompt-Enhance (aus: Schalter und Textgenerator entfernen, Prompt geht direkt in den Text-Encoder)
    for k in api.values():
        if k['class_type'] == 'ResizeImageMaskNode':
            k['inputs'] = {'input': k['inputs']['input'], 'resize_type': 'scale longer dimension',
                           'resize_type.longer_size': 1536, 'scale_method': 'lanczos'}
    for i in [i for i, k in api.items() if k['class_type'] == 'ComfySwitchNode']:
        ersatz = api[i]['inputs']['on_false']
        for a in api.values():
            for n, v in a['inputs'].items():
                if v == [i, 0]:
                    a['inputs'][n] = ersatz
        api.pop(i)
    for i in [i for i, k in api.items() if k['class_type'] == 'TextGenerateLTX2Prompt']:
        api.pop(i)

    # Die Widget-Eingaben des Subgraphen (ohne Link) wirken ueber die Proxy-Verbindungen schon oben.
    # Eingangsbild und Ausgabe-Praefix setzen
    for k in api.values():
        if k['class_type'] == 'ResolutionSelector':
            if aspect:
                k['inputs']['aspect_ratio'] = aspect
            if megapixel:
                k['inputs']['megapixels'] = megapixel
        if k['class_type'] == 'LoadImage':
            k['inputs']['image'] = bild
        if k['class_type'] == 'SaveVideo':
            k['inputs']['filename_prefix'] = praefix
            k['inputs'].setdefault('format', 'auto')
            k['inputs'].setdefault('format.codec', 'auto')
    return api


if __name__ == '__main__':
    import sys
    p = baue(sys.argv[1], 'x.png', 'test', 'ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors', 11)
    print(json.dumps(p, indent=1)[:6000])
    print(len(p), 'Knoten')
