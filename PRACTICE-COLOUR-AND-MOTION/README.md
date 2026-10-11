# Colour an image, then animate that result

![Actual colour result](example/COLORIZED.png)

Open `workflows/01-COLOUR.workflow.json` in ComfyUI. Choose `example/GRAYSCALE.png` in Load Image, select the three image models in the loaders, and click Run. The reference image is VAE-encoded and connected to both Reference Latent branches. Seed24, Euler, four steps, CFG1,1536x864.

Save the chosen colour PNG, then open `02-ANIMATE.workflow.json` and select that PNG. Copy the two supplied conditioning files to your ComfyUI embeddings folder, or use the runner below to keep them in its own output directory. For this example they contain our already executed town-motion prompt. For a different motion request, encode and save new files with `03-SAVE-MOTION-PROMPTS` and point the video graph at them.

## Run the same example in separate owned processes

Install `psutil` in the Python environment you already use for ComfyUI. Put the model weights in the paths listed in [MODEL-FOLDERS.md](MODEL-FOLDERS.md); [MODELS.json](MODELS.json) pins each full hash and source. Then run from this extracted folder:

```powershell
python run_colour_motion.py --comfyui C:\AI\ComfyUI --python C:\AI\venv\Scripts\python.exe --output C:\AI\my-colour-and-motion
```

To try only the colour stage, add `--colour-only`. To supply a different starting image, add `--input C:\Images\my-image.png`. The example keeps a1536x864 output canvas; adjust both size fields in the colour API graph for other shapes.

Results are `results/COLORIZED.png` and `results/ANIMATED.mp4`. The runner refuses an existing output directory or occupied port. It starts a separate process for each stage, saves request/result records and RAM samples, and stops only those owned processes. The video stage defaults to `--reserve-vram16`, our recorded64GB Strix Halo Windows profile; this is not a measured NVIDIA12GB profile.

## Files to keep beside ComfyUI

- `example/`: our own generated grayscale input, actual colour output and completed short clip.
- `workflows/`: directly openable UI graphs and the API request graphs.
- `embeddings/`: the positive/negative motion conditioning used in this example.
- [SETUP-WINDOWS-AMD.md](SETUP-WINDOWS-AMD.md): pinned setup notes from our earlier practical image/clip run. The recording used an existing installation and driver.
- `NATIVE-COLOUR-VALIDATION.json` and `NATIVE-MOTION-VALIDATION.json`: actual local run records. Separate runner-download validation is recorded when that run has completed.

Colours are generated choices for our fictional town. They are not evidence of historical colours. Original image files are kept separate. Model weights retain their own source terms and are not included here.
