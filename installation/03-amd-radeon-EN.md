# AMD Radeon: proposed local test route

No independent Radeon card has been tested here. Strix Halo evidence is a separate hardware case.

Record exact GPU, VRAM, OS and driver. Compare them with AMD's official OS/GPU/framework matrix, including its version selector: https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html

Use official ComfyUI Desktop for supported AMD hardware or the matching AMD PyTorch instructions. Do not copy CUDA commands or the Strix Halo gfx1151 setup onto a different Radeon. Keep a separate installation. Do not disable Windows security features.

Verify GPU recognition in the startup log. First run one greeting-card image, batch size one and no concurrent model workload. The archived Windows ROCm 7.2.1 matrix lists FP8 for RDNA4 only; our FP8/INT8 graph is not automatically compatible with every Radeon. A BF16 variant is a separate untested configuration, not a renamed FP8 file.

Only try LTX after a successful image test. Record complete errors and actual memory use. Fill TESTPROTOKOLL-EN.md. Successful import alone does not establish inference compatibility. Current ComfyUI docs and older AMD docs refer to different software generations; do not mix package commands across them.
