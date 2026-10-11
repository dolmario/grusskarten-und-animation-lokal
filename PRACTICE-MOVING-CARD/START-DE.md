# Bild und Grußkarte animieren, Schrift ruhig halten

Das Beispiel verbindet unseren tatsächlich erzeugten LTX-Clip mit einer festen Schriftlage. Öffne das lokale Werkzeug, gib den Gruß ein, wähle Position und Größe und klicke auf Export MP4. Jede Fassung bleibt in einem eigenen Unterordner erhalten.

Die Startbefehle stehen in README.md. Eine neue Python-Umgebung mit Pillow12.3.0 wird im entpackten Ordner angelegt; FFmpeg muss auf PATH verfügbar sein. Danach http://127.0.0.1:18192 öffnen. Für einen eigenen vorhandenen Clip `--clip C:\Images\mein-clip.mp4` und einen neuen Ausgabeordner angeben.

Der ComfyUI-Graph für das Startbild liegt bei. Für einen anderen Bewegungswunsch neues Conditioning mit dem getrennten Speichergraphen erzeugen. Unsere gelieferten Dateien stammen aus dem ausgeführten Gemma-Textlauf für die Stadt. Clip-Erzeugung und nachträglicher Kartenexport sind getrennte Schritte. Schriftänderungen rechnen den LTX-Clip nicht erneut.

Eigene erzeugte Beispielbilder, keine privaten Fotos und keine Modellgewichte im Download. Modellbedingungen gelten getrennt. Der neue Film hat englischen Ton und deutsche Untertitel; menschliches Vollhören bleibt gesondert offen.
