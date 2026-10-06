# Die passenden Modelldateien

Für die erste Grußkarte nur die drei Zeilen **card** laden: zusammen 12,45 GB auf der SSD, zusätzlich benötigt ComfyUI Platz und Arbeitsspeicher. Dateigröße ist keine VRAM-Mindestanforderung. Die großen LTX-Dateien erst für Teil 2 laden. Qwen ist eine optionale andere Bild-KI.

| Aufgabe | Ziel relativ zum ComfyUI-Ordner | Offizielle Datei | Downloadgröße |
|---|---|---|---|
| card | `models/diffusion_models/flux-2-klein-4b-fp8.safetensors` | [Download](https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8/resolve/main/flux-2-klein-4b-fp8.safetensors) | 4.07 GB |
| card | `models/text_encoders/qwen_3_4b.safetensors` | [Download](https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-4b/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors) | 8.04 GB |
| optional_qwen | `models/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors` | [Download](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors) | 20.43 GB |
| optional_qwen | `models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors` | [Download](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors) | 9.38 GB |
| optional_qwen | `models/vae/qwen_image_vae.safetensors` | [Download](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors) | 0.25 GB |
| card | `models/vae/flux2-vae.safetensors` | [Download](https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors) | 0.34 GB |
| animation | `models/vae/ltx-2.5-video-vae-bf16.safetensors` | [Download](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/vae/ltx-2.5-video-vae-bf16.safetensors) | Größe nicht archiviert |
| animation | `models/vae/ltx-2.5-audio-vae-bf16.safetensors` | [Download](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/vae/ltx-2.5-audio-vae-bf16.safetensors) | Größe nicht archiviert |
| animation | `models/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors` | [Download](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors) | Größe nicht archiviert |
| animation | `models/text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors` | [Download](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors) | Größe nicht archiviert |
| animation | `models/diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors` | [Download](https://huggingface.co/Lightricks/LTX-2.5/resolve/main/diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors) | Größe nicht archiviert |

1. In deiner ComfyUI-Installation den Ordner `models` öffnen. Bei Desktop die Modellbibliothek deiner aktiven Installation öffnen; sie kann außerhalb des Programmordners liegen.
2. Datei in den genannten Unterordner legen. Nicht die Hugging-Face-HTML-Seite speichern. Unter Windows die Dateinamenerweiterungen anzeigen. Keine Endung `.html`, keine doppelte `.safetensors.safetensors`.
3. ComfyUI neu starten, wenn die Auswahllisten die Datei noch nicht anbieten. Im jeweiligen Loader den Dateinamen auswählen.
4. Optional mit `python werkzeuge/pruefe_modelle.py PFAD_ZU_COMFYUI` prüfen. Es werden ausschließlich vorhandene Dateien gelesen; nichts geladen oder installiert.

LTX erfordert derzeit einen Hugging-Face-Zugang und eigene Zustimmung zu den Anbieterbedingungen. Dieser Download wird nicht stellvertretend freigeschaltet. Der Prompt-Enhancer ist im angebotenen Testgraph nicht erforderlich. Die Distilled- und Dev-Dateien niemals einfach austauschen. Die Parameter gehören zur Modellvariante.

Mac: Dieses archivierte FP8/INT8-Paket ist keine getestete MPS-Variante. Siehe `04-mac-DE.md`.
