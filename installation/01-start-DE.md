# Schritt 1: ComfyUI einrichten

Ein Workflow ist ein fertiger Bauplan. ComfyUI führt diesen Bauplan auf deinem Rechner aus; die Modelldateien sind die benötigten KI-Bauteile. Unser kleines ZIP enthält den Bauplan und die Anleitung, aber keine riesigen Modelle und keinen versteckten Cloud-Dienst.

## Wenn ComfyUI schon läuft

Deine funktionierende Installation behalten. Adresse aus ihrem Startfenster öffnen (in unseren Archivtests meist http://127.0.0.1:8189). Erst die erste Grußkarte importieren. Nicht alles neu installieren oder mehrere Server auf demselben Port starten.

## Neue Installation für Anfänger

1. [Offiziellen Download öffnen](https://www.comfy.org/download). Windows: passende Windows-Ausgabe; Mac: Apple-Silicon-Ausgabe.
2. Installer ausführen. Einen eigenen leeren Ordner/ eine eigene neue Installation verwenden und den Modellordner notieren. Die vorhandene funktionierende Installation behalten.
3. Bei der Hardwarewahl deinen tatsächlichen Grafikchip wählen. NVIDIA und AMD sind unterschiedliche Wege. Für AMD zuerst 03-amd-radeon-DE.md lesen.
4. ComfyUI starten. Du solltest eine Zeichenfläche für verbundene Kästchen sehen. In der aktuellen Desktop-Version gegebenenfalls zuerst eine ComfyUI-Instanz anlegen/öffnen. Oberfläche und Beschriftungen können sich mit der Version ändern.
5. Noch keine Modelle wahllos herunterladen. Zuerst Aufgabe und Plattform auswählen, dann 02-modelle-DE.md lesen.

[Windows-Anleitung](https://docs.comfy.org/installation/desktop/windows), [Mac-Anleitung](https://docs.comfy.org/installation/desktop/macos), [Hardwareanforderungen](https://docs.comfy.org/installation/system_requirements). Der aktuelle Desktop-Neuinstallationsweg wurde hier recherchiert, nicht frisch installiert. Unsere belegten lokalen Ergebnisse stammen aus der archivierten manuellen Installation mit ComfyUI-Commit fa98a189b4271c76f66210e15f81790b555eb610 (Frontend 1.53.10). Installationsversionen nicht mit Laufzeitbelegen verwechseln.

Keine behauptete universelle Mindestgröße oder Laufzeit: großer Bildencoder, Bildgröße, Videozahl und Auslagerung beeinflussen den Speicherbedarf. Für einen schwachen PC zunächst prüfen, ob die konkrete Aufgabe passt. LTX ist erheblich anspruchsvoller als ein einzelnes Kartenbild.
