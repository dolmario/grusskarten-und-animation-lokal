# Schwarzweissbild kolorieren und animieren

Öffne `workflows/01-COLOUR.workflow.json` in ComfyUI, wähle `example/GRAYSCALE.png` in Load Image und die drei passenden Bildmodelle. Run erzeugt die Farbversion. Das Bild geht über VAE Encode als Referenz in BEIDE Reference-Latent-Zweige. Beispiel: Seed24/fixed, Euler,4Schritte,CFG1,1536x864.

Speichere die gewählte PNG. Öffne danach `02-ANIMATE.workflow.json` und wähle sie als Eingang. Die zwei gelieferten Conditioning-Dateien kommen in ComfyUIs embeddings-Ordner. Sie stammen aus unserem bereits ausgeführten Gemma-Bewegungstextlauf. Für einen geänderten Bewegungswunsch neue Conditioning-Dateien mit dem separaten Speichergraphen erzeugen.

Der Runner hält diese Dateien in seinem eigenen neuen Ausgabeordner und startet Bild und Video in getrennten eigenen Prozessen. Befehle und Downloads stehen in README.md und MODEL-FOLDERS.md. Fertige Ergebnisse: results/COLORIZED.png und results/ANIMATED.mp4. Filmton Englisch, deutsche Untertitel; bestehende Installation/Treiber, kein behaupteter NVIDIA-Zielrechnertest.

Unser Beispielbild ist eine eigene erzeugte Stadt in Graustufen. Die neuen Farben sind eine Interpretation. Gewichte separat nach jeweiligen Modellbedingungen herunterladen. Menschliches Vollhören/Vollsehen des neuen Tutorials bleibt gesondert offen.
