# Mac: Apple Silicon, als Testweg vorbereitet

**Nicht auf einem Mac praktisch getestet. Kein fertiger Mac-LTX-Kompatibilitätsnachweis.**

1. Apple-Menü → Über diesen Mac: Apple-Silicon-Chip, macOS und gemeinsamen Speicher notieren. Die offizielle Desktop-Anleitung nennt macOS 13 oder neuer und M1 oder neuer. Ein Intel-Mac wird damit nicht als passender Desktop-Weg bestätigt.
2. [Offizielle Mac-Anleitung](https://docs.comfy.org/installation/desktop/macos) öffnen, offiziellen .dmg-Download verwenden, App nach Programme ziehen, Comfy Desktop starten und eine eigene Instanz anlegen/öffnen. Kein CUDA-/ROCm-Installer auf dem Mac.
3. ComfyUI verwendet laut [Dokumentation](https://docs.comfy.org/installation/system_requirements) PyTorch/MPS (Metal), nicht MLX. Der Modellordner kann unter der gemeinsamen Modellbibliothek liegen; den tatsächlichen Pfad der aktiven Instanz notieren.
4. Zuerst kleines Bild als Hardwaretest. Unsere archivierten FP8-/INT8-Dateien NICHT als garantiert MPS-tauglich ansehen. Als Rechercheansatz existiert [FLUX.2 Klein 4B BF16](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B); der Anbieter erwähnt MPS. Das beweist noch keinen Lauf unseres ComfyUI-Graphs. Lade keine große Modellfamilie vor der Prüfung.
5. Der Mac-Weg braucht gegebenenfalls einen passenden BF16/FP16-ComfyUI-Checkpoint und passende Loader. Die genaue Dateizuordnung bleibt bis zur Prüfung dieser Kombination offen. Keine FP8-Datei einfach in BF16 umbenennen. Wir liefern bewusst keinen angeblich fertig getesteten Mac-Workflow.
6. LTX erst nach gesonderter Prüfung von Modell-Datentypen, Nodes und Speicher. Eine unterstützte ComfyUI-App bedeutet nicht, dass jedes Video-Modell unterstützt ist. Keine generierten Mac-Laufzeitversprechen.
7. `TESTPROTOKOLL-DE.md` ausfüllen: Import, GPU-Erkennung, echte Ausgabe, Fehler und Dateiprüfung getrennt notieren.

Für das Tutorial kannst du alle Schritte und Prompts nachlesen; die tatsächliche Mac-Inferenz bleibt ein offener Praxistest.
