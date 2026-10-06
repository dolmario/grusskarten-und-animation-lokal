# AMD-Radeon-Grafikkarten: vorbereiteter Testweg

**Noch kein eigener Lauf auf einer separaten Radeon-Grafikkarte. Strix Halo ist ein anderer Hardwarefall.** Wir behaupten weder eine Laufzeit noch eine komplette Kompatibilität.

1. Exakte Karte, VRAM, Windows-/Linux-Version und Treiber notieren. Unter Windows im Task-Manager → Leistung → GPU nachsehen.
2. Karte plus Betriebssystem in der [AMD-Kompatibilitätsmatrix](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html) bzw. aktuellen Nachfolgedokumentation vergleichen. Die verlinkte 7.2.1-Matrix nennt nur bestimmte Karten; nicht jede Radeon ist dadurch abgedeckt.
3. Den offiziellen ComfyUI-Desktop-Weg für unterstützte AMD-Hardware wählen. Bei manueller Installation die exakt zur Karte und zum OS passende [AMD-PyTorch-Anleitung](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/windows/install-pytorch.html) nutzen. NVIDIA-CUDA-Befehle oder unseren gfx1151-Strix-Halo-Weg nicht ungeprüft übernehmen.
4. Installation getrennt halten. Keine Windows-Sicherheitsfunktion oder Schutzsoftware für diesen Versuch abschalten. Nicht auf einem fremden PC ohne dessen Besitzer installieren.
5. Zuerst ComfyUI starten und GPU-Erkennung im Startprotokoll prüfen. Danach mit der ersten Karte beginnen, batch_size 1, keine parallele andere Modelllast.
6. FP8 beachten: In AMDs archivierter 7.2.1-Windows-Matrix wird FP8 nur für RDNA4 angegeben. Unser FP8-/INT8-Archiv ist deshalb nicht automatisch für jede AMD-Karte geeignet. Bei Datentypfehlern stoppen und die konkrete Backend-/Modellkombination prüfen. BF16 ist eine mögliche separate Variante, hier nicht getestet und nicht durch bloßes Umbenennen einer FP8-Datei herstellbar.
7. Erst nach erfolgreichem Kartenbild LTX versuchen. Bei Speicherfehlern Fehlertext, Auflösung und Spitzenbelegung sichern, nicht mit Register-/BIOS-Tricks kaschieren.
8. `TESTPROTOKOLL-DE.md` ausfüllen. Ein Import ohne Bild ist kein bestandener Modelltest.

Die neuesten ComfyUI- und älteren AMD-Seiten nennen unterschiedliche Softwaregenerationen. Wir mischen deren Paketbefehle nicht. Der Versuch muss eine konsistente, für deine Karte offiziell unterstützte Generation verwenden.
