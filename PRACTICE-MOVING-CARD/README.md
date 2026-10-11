# Make a moving greeting card from your local clip

Open the local card tool, type the message, choose its position and export MP4. The background moves while the message is a separate fixed overlay. The example uses our actual recorded LTX town clip and does not regenerate that clip when you change the greeting.

## Start on Windows

Install Python3.12 or use your existing installation. Install FFmpeg from the [official download page](https://ffmpeg.org/download.html) and make its `bin` directory available on PATH. The recording used existing FFmpeg9.0.1 and a newly created Python environment with [Pillow12.3.0](https://pypi.org/project/pillow/12.3.0/).

From the extracted kit folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ffmpeg -version
.\.venv\Scripts\python.exe card_studio.py --output my-moving-cards
```

Open `http://127.0.0.1:18192` in your browser. Type the message and click **Export MP4**. Download the finished file, or find it together with the actual FFmpeg command and result record under `my-moving-cards/<export-id>/`.

Use a clip from your own ComfyUI session:

```powershell
.\.venv\Scripts\python.exe card_studio.py --clip C:\Images\my-ltx-clip.mp4 --output my-next-cards
```

Each start uses a new output directory. An occupied port is preserved; choose `--port18193` with a space between option and value if needed. The supplied Windows default font is Segoe UI Bold from the existing system; the font file is not bundled. Use `--font C:\Fonts\my-font.ttf` for another installed TrueType font. Stop the foreground server with Ctrl+C after exports finish.

## Get your picture into motion

The included ComfyUI motion graph uses the supplied `COLORIZED.png` as its visual starting point. Upload that PNG in Load Image. Copy the two provided `.safetensors` conditioning files into ComfyUI's `models/embeddings/` folder, select the model files listed in MODEL-FOLDERS.md, and run the graph. These conditioning files contain our already executed town-motion text; use the separate prompt-saving graph to encode a changed movement request.

The recorded base clip is121frames at24fps,1280x704. Initial latent640x352,8steps,2xlatent upscale,3refinement steps. The native source generation was actually clicked and completed in the earlier colour-and-motion example. The card export is a separate CPU FFmpeg operation. Card output is1280x720,H264,24fps with a fixed PNG text overlay; it has no soundtrack. Newer GPU experiments or NVIDIA execution are not implied by this reuse.

The recording used an existing ComfyUI installation on64GB Strix Halo with a16GiB video reserve. Setup notes and the actual model downloads are provided separately. No model weights or private photographs are included.

## Example results

`example/SOURCE.mp4`: actual LTX output. `example/CARD-GERMAN.mp4`: "Alles Gute!" at the bottom. `example/CARD-BIRTHDAY.mp4`: "Happy Birthday!" at the top. `VALIDATION.json` records actual exports and download verification when completed. English tutorial narration with German subtitles; human whole-film listening/viewing remains separate.
