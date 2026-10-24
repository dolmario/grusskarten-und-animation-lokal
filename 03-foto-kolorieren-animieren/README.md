# Alte Fotos kolorieren und animieren (lokal, ohne Cloud)

Rezept zum Video „Alte Fotos kolorieren und animieren: kostenlos, lokal, ohne Cloud“ auf dem Kanal Dolmario Local AI.
Das Beispielfoto in `beispiel/` ist KI-erzeugt und zeigt keine realen Personen.

## Ablauf

1. **Foto sichern:** Ein schiefes Handyfoto vom Abzug genügt. `werkzeuge/entzerren.py` findet den hellen Papierrand, entzerrt den Abzug und schneidet ihn zu (`python entzerren.py eingabe.png ausgabe.png [rand_px]`, benötigt numpy und Pillow). Ein Abzug ganz ohne hellen Rand wird womöglich nicht erkannt.
2. **Kolorieren:** FLUX.2 Klein 4B Edit, Farb-Prompt in `farb-prompt.txt`. Die Farben im Prompt benennen, denn aus Grautönen lässt sich nicht erraten, welche Farbe Kleid, Anzug oder Blumen hatten. Die Farben sind eine Vermutung, keine Geschichte. Mehrere Seeds rechnen und Gesichter prüfen.
3. **Animieren:** LTX-2.5 22B distilled, Bildstärke 1,0, feste Kamera, 5 s, 24 fps, Prompt in `bewegungs-prompt.txt`. Drei Regeln: kein Kuss Mund auf Mund (die Nasen verschmelzen), ein Satz über die Augen, feste Kamera. Gesichter jede Sekunde prüfen.

## Gemessen

- AMD-Mini-PC (Ryzen AI Max+ 395, Radeon 8060S, 64 GB, Windows 11): Farbe etwa 20–40 s, Clip 640x832 etwa 4 min, einstufig. Die zweite Hochskalierungsstufe ist dort zweimal abgestürzt.
- RTX 3090 Ti: Clip 832x1088 in etwa 75 s mit zweiter Stufe (`ti-workflow/`, ComfyUI-Vorlage `video_ltx2_5_i2v` als API-Workflow).
- Andere Grafikkarten haben wir nicht getestet.

## Dateien

| Datei | Inhalt |
|---|---|
| `farb-prompt.txt`, `bewegungs-prompt.txt` | die beiden Prompts |
| `werkzeuge/entzerren.py` | Handyfoto entzerren und zuschneiden |
| `ti-workflow/` | Läufer und Vorlage der RTX-3090-Ti-Fassung (`kolorieren.py`, `ltx_lauf.py`, `ltx_api.py`, `modelle.json` mit Download-Quellen und Prüfsummen) |
| `beispiel/` | erfundenes Handyfoto, Schwarzweiß, koloriert, animiert |

Bitte vor kommerzieller Nutzung die Lizenz jedes Modells prüfen (FLUX.2 Klein, LTX-2.5). Eigene oder erfundene Fotos nehmen, keine Fotos fremder Menschen ohne Einverständnis, KI-Bilder als KI kennzeichnen.

---

# Colorize and animate old photos (local, no cloud)

Recipe for the Dolmario Local AI video. The example photo in `beispiel/` is AI-generated and shows no real people.

1. **Save the photo:** a crooked phone photo of the print is enough. `werkzeuge/entzerren.py` finds the light paper border, straightens and crops the print (needs numpy and Pillow; a print without a light border may not be detected).
2. **Colour:** FLUX.2 Klein 4B Edit with `farb-prompt.txt`. Name the colours in the prompt. The colours are a guess, not history.
3. **Motion:** LTX-2.5 22B distilled, image strength 1.0, fixed camera, 5 s, 24 fps, `bewegungs-prompt.txt`. No mouth kiss (the noses melt), one sentence about the eyes, fixed camera.

Measured: AMD mini PC about 4 min per clip at 640x832 (single stage, the second stage crashed it twice); RTX 3090 Ti about 75 s at 832x1088. Other graphics cards not tested. Check each model's licence before commercial use.