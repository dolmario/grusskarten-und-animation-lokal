# Deine erste lokale KI-Grußkarte

## 1. Das kleine Paket herunterladen

Auf der Hauptseite auf **Grußkarten: Downloadpaket** klicken, ZIP speichern und komplett entpacken. Windows: Rechtsklick → Alle extrahieren. Mac: ZIP doppelklicken. Danach START-DE.md öffnen. Dateien nicht direkt aus dem ZIP in ComfyUI ziehen. Modelle sind nicht im ZIP.

## 2. ComfyUI öffnen und Modelle bereitlegen

In installation/01-start-DE.md deinen Installationsweg auswählen. Für dieses Beispiel FLUX.2 Klein **4B Distilled** verwenden. Genau die drei **card**-Dateien in installation/MODELS.json laden und in die angegebenen Modell-Unterordner legen. Nicht Base, 9B oder Dev auswählen.

## 3. Fertigen Bauplan importieren

`workflows/01-grusskarte-klein4.ui.json` auf die ComfyUI-Zeichenfläche ziehen. Alternativ Workflow-Menü → Open/Öffnen. Die `.api.json` ist eine technische Beilage, nicht der Anfänger-Import. Jetzt sind die Kästchen bereits verbunden. Keine Kabel neu erfinden.

## 4. Drei Loader kontrollieren

UNETLoader: `flux-2-klein-4b-fp8.safetensors`. CLIPLoader: `qwen_3_4b.safetensors`, Typ `flux2`. VAELoader: `flux2-vae.safetensors`. Fehlt ein Name, Pfad/Dateiendung prüfen und bei Bedarf ComfyUI neu starten. Rote fehlende Nodes: passende ComfyUI-Version in einer getrennten Installation prüfen; für diesen Graph werden keine frei erfundenen Custom Nodes verlangt.

## 5. Was wird auf der Karte stehen?

Im Kästchen **CLIPTextEncode · 4** steht der gesamte Bildwunsch. Unser Originalprompt liegt unter prompts/01-geburtstag.txt. Er beschreibt das Motiv auf Englisch und fordert die deutschen Zeilen „Alles Gute, Werner!“ und „70 Jahre jung!“. Zum eigenen Test nur Motiv, Name und Anlass ändern. Namen in Anführungszeichen setzen. Die KI kann trotzdem Buchstaben vertauschen.

## 6. Einstellungen zunächst beibehalten

Flux2Scheduler und EmptyFlux2LatentImage: beide 1088 × 1088. Der Prompt nennt zwar 1080, die tatsächlichen Nodewerte bestimmen hier 1088. Steps 4; CFGGuider 1; KSamplerSelect euler; RandomNoise Seed 11; batch_size 1. Seed-Nachlauf fixed. Diese Kombination gehört zu 4B Distilled. Wenn du die Größe änderst, beide Größen-Kästchen passend ändern, nicht nur eines.

## 7. Ein Bild berechnen

Run / Queue Prompt einmal drücken. Warten, bis die Aufgabe beendet ist. Nicht mehrfach klicken, solange sie läuft. Es gibt keine zugesicherte Zeit für deinen Rechner. Bei einer roten Fehlermeldung zum Abschnitt Fehlerhilfe wechseln.

## 8. Karte finden und wirklich speichern

Die letzte Node heißt **SaveImage · 13**, Präfix `karte_klein_geburtstag-1x1_11`. Die tatsächliche PNG liegt im output-Ordner deiner aktiven ComfyUI-Installation bzw. Ausgabe-Bibliothek. Am Vorschaubild Rechtsklick → Save Image/Save image as oder entsprechende Download-Schaltfläche, je nach Oberfläche. Nicht nur einen Screenshot speichern. Die PNG in einen eigenen Ergebnisordner kopieren.

## 9. Alles Gute, Wermer?

Die vorhandene Klein-4B-Ausgabe im Ordner examples zeigt tatsächlich „Wermer“. Dieser Workflow lief technisch erfolgreich, die Schreibweise ist trotzdem falsch. Die Qwen-Kontrolle trifft den Namen Werner, schreibt aber „Gutte“ statt „Gute“. Sie ist ebenfalls fehlerhaft und stammt aus einem anderen Modell. Vor Versand jedes Wort bei voller Größe lesen. Bei Fehlbuchstaben neu versuchen oder das Bild ohne Aufschrift erzeugen und den Text in deinem vertrauten Bildeditor ergänzen. Das ist keine automatische Textkorrektur des Workflows.

## 10. Neue Varianten und Übergabe an Teil 2

Für neue Bilder Seed ändern; für einen sauberen Vergleich nur eine Einstellung zugleich ändern. Prompt, Workflow, Seed und PNG zusammen aufheben. Unter output liegt die fertige Karte; diese PNG kannst du in Teil 2 in LoadImage öffnen. Ein PNG-Dateiname garantiert noch keine Transparenz. Für Sticker den Alphakanal gesondert prüfen.

## Fehlerhilfe

- Modell nicht auswählbar: Dateiname, Unterordner, Dateigröße prüfen. Eine HTML-Loginseite ist kein Modell.
- Missing node: unterstützte Version/Startprotokoll prüfen. Unser Graph stammt aus der archivierten Installation; aktuelle stabile Builds können neue Nodes noch nicht enthalten.
- Out of memory: keine parallele Bild-/Video-KI; batch_size 1; kleinere passende Größe in beiden Nodes testen. Wenn es weiter scheitert, stoppen und Testprotokoll ausfüllen.
- Falscher Name: Das ist ein Bildqualitätsfehler, kein fehlendes Kabel.
- Mac/Radeon-Datentypfehler: eigene Plattformhinweise lesen; FP8/INT8 nicht universell voraussetzen.

Status: Original-API samt History belegt einen erfolgreichen Strix-Halo-Einzeltest. Die neue Anfänger-UI wurde aus realen exportierten Nodes aufgebaut und statisch exakt gegen das API geprüft; frischer UI-Reimport und erneute Inferenz sind separat offen. Zusatz-Qwen-UI-Dateien wurden früher importiert/reimportiert geprüft. Keine neue Radeon-/Mac-Ausführung behauptet.
