# Model files

For the first card download only the three **card** entries in MODELS.json: approximately 12.45 GB of files, plus ComfyUI and working space. Disk size does not establish required VRAM. Animation uses a separate, larger LTX model set. Optional Qwen is a different image model.

Open the active ComfyUI model library. Save each official file to exactly the relative `path` in MODELS.json. Keep the complete filename and extension; a downloaded HTML page is not a model. Restart ComfyUI if filenames are missing from loader dropdowns.

Optional read-only check: `python werkzeuge/pruefe_modelle.py PATH_TO_COMFYUI`. It reads installed files, verifies available archived hashes and never downloads or installs anything.

LTX downloads currently require your own Hugging Face access and acceptance of the vendor's terms. Do not swap Distilled for Dev without its matching workflow. This graph does not require the optional prompt enhancer.

The archived FP8/INT8 setup is not a validated Mac/MPS setup. Read 04-mac-EN.md before downloading.
