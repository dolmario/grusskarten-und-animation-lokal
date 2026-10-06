# Aus einem Bild ein kleines Video machen

## 1. Vorbereiten

Das Animations-ZIP auf der Hauptseite herunterladen und komplett entpacken. Wir verwenden LTX-2.5 **Distilled**, nicht die Dev-Datei. ComfyUI zuerst mit einer funktionierenden Installation öffnen; installation/01-start-DE.md lesen. Noch keinen fremden Rechner verändern. Mac und separate Radeon bleiben ungetestete Plattformwege.

## 2. Modelle getrennt laden

In installation/MODELS.json nur die fünf **animation**-Dateien auswählen: Diffusionsmodell, Gemma-Textencoder, Video-VAE, Audio-VAE und räumlicher Upscaler. Der Audio-Zweig gehört intern zum vorhandenen Graph, obwohl das gespeicherte Video keinen Audiostream erhält. Kein zusätzlicher Prompt-Enhancer erforderlich. LTX-Zugang und Bedingungen auf Hugging Face selbst prüfen; die Gewichte fehlen absichtlich im kleinen ZIP.

## 3. Bauplan öffnen

`workflows/01-archivfoto-ltx25.ui.json` auf die Zeichenfläche ziehen. Die `.api.json` nur als technische Beilage verwenden. Nicht alle Kabel nachbauen: der fertige Bauplan enthält beide Rechenstufen und den Export.

## 4. Bild laden

Node **LoadImage · 1**: Upload/choose file anklicken und `input/07-schmied-1850-1860_seed11.png` wählen. Das ist eine bereits KI-kolorierte Interpretation eines dokumentierten Archivfotos, kein privates Familienbild. Alternativ deine fertige Karte aus dem ersten Tutorial laden; das ist ein neuer Versuch, kein identischer Archivlauf. Erlaubnis/Rechte am eigenen Eingangsbild vorher prüfen.

## 5. Was sich bewegen soll

In **CLIPTextEncode · 5** steht der tatsächlich benutzte kurze Originalprompt. Einen ruhigen ausführlicheren Vorschlag findest du in prompts/02-ruhige-bewegung-vorschlag.txt; er ist ausdrücklich noch ungetestet. Mit einer kleinen Bewegung anfangen. Kamera festhalten, keine neuen Gegenstände oder Gesichter verlangen. Schrift auf Karten kann sich trotz dieser Anweisung verändern.

## 6. Modellnamen kontrollieren

UNETLoader · 7 lädt Distilled. CLIPLoader · 4 lädt den Gemma-Encoder, Typ ltxv. VAELoader · 8 ist Video, · 9 Audio. LatentUpscaleModelLoader · 21 ist der LTX-Upscaler. Die genauen Namen stehen in MODELS.json. Nicht durch ähnlich klingende LTX-2.0-/2.3-Dateien ersetzen.

## 7. Größe, Länge und beide Stufen verstehen

Die genauen Werte des angebotenen Originaltests stehen unverändert im Workflow und PARAMETERS.json. Die erste Stufe beginnt kleiner, die zweite vergrößert räumlich. Framezahl ist nicht die Zahl der Sekunden: ungefähr Frames geteilt durch FPS. Für Vergleiche immer denselben Seed und dieselbe Länge behalten. Ein anderer Prompt oder kürzerer Lauf ist ein eigener Versuch.

Die manuell gespeicherten Sigma-Folgen, Video-/Audio-CFG und zweite Stufe gehören zu Distilled. Nicht für Dev übernehmen. Bei eigener Längenänderung EmptyLTXVLatentVideo.length und LTXVEmptyLatentAudio.frames_number gemeinsam ändern; FPS in Conditioning, Audio und CreateVideo konsistent halten. Zum ersten Nachbau zunächst nichts davon verändern.

## 8. Einmal starten

Run / Queue Prompt einmal drücken. Video braucht wesentlich mehr Ressourcen als eine Karte; kein pauschales Zeitversprechen. Eine laufende Aufgabe nicht versehentlich mehrfach einreihen. Bei Speicherfehlern den vollständigen Fehler und deine Hardware festhalten, nicht mehrfach blind neu starten.

## 9. MP4 finden

Die letzte Node **SaveVideo · 33** schreibt MP4/h264 unter dem im Graph angegebenen Präfix. Dieser relative Pfad liegt unter dem output-Ordner der aktiven ComfyUI-Installation. Den fertigen Film dort mit einem normalen Player öffnen. Speichere die tatsächliche MP4 zusammen mit PNG, Prompt und Workflow.

## 10. Video beurteilen, bevor du es verschickst

Anfang, Mitte und Ende ansehen. Bleiben Gesicht, Hände, Hammer, Hufeisen, Bildrand und Hintergrund gleich? Bei Grußkarten jedes Wort über die gesamte Dauer prüfen. Ein technisch fertiger Film kann trotzdem Werkzeuge verformen, die Kamera zoomen oder Schrift verändern. Genau solche Fehler gibt es in unseren alten Ergebnissen. Ein bewegtes Archivfoto ist eine KI-Interpretation, keine historische Filmaufnahme.

## Fehlerhilfe

Missing node → Version/Startprotokoll prüfen. Modell fehlt → Dateiname, Zielordner und Zugangsstatus prüfen. Falsche Datei-/Loginseite → Download korrigieren. Out of memory → keine parallele Modelllast, Größe/Länge passend reduzieren und beide gekoppelten Werte beachten; Fehlerprotokoll führen. Keine Dev-Näherung als offiziell getesteten Dev-Workflow verkaufen.

Status: Originalgraph und vorhandener Originalclip stammen aus dem Strix-Halo-Test. Neue UI statisch exakt mit diesem API abgeglichen, frischer UI-Reimport und neue Inferenz offen. NVIDIA-Zusatzdateien stammen aus getrennten Archivtests. Keine neue Radeon-/Mac-Laufzeit oder Garantie.
