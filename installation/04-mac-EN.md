# Mac / Apple Silicon: research route, not a validated model setup

No Mac execution has been performed. The official Desktop guide lists macOS 13 or newer and M1 or newer: https://docs.comfy.org/installation/desktop/macos

Record chip, macOS and unified memory. Download the official DMG, drag the app to Applications, start Desktop and open/create a separate ComfyUI instance. Use its actual model-library path. Do not install CUDA or ROCm on the Mac. ComfyUI uses PyTorch/MPS (Metal), not MLX.

The archived FP8/INT8 files are not guaranteed to work on MPS. The BF16 FLUX.2 Klein 4B model page mentions MPS: https://huggingface.co/black-forest-labs/FLUX.2-klein-4B . This is a research lead, not proof for our ComfyUI graph. Exact compatible BF16/FP16 checkpoint/loader mapping remains open until tested; renaming FP8 weights does not convert them.

First verify a small image on the actual Mac. LTX requires a separate dtype/node/memory check. App installation support is not video-model compatibility. Record real outputs and errors in TESTPROTOKOLL-EN.md. No Mac runtime or memory guarantees are claimed.
