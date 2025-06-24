set HF_HOME=%CD%\.caches\hf_download
@REM set HF_ENDPOINT=https://hf-mirror.com

.venv\Scripts\python.exe facefusion.py run --open-browser --temp-path .caches\temp --output-path D:\adult\output --temp-frame-format jpeg --output-audio-encoder aac --face-swapper-model hyperswap_1a_256 --face-swapper-pixel-boost 1024x1024 --face-occluder-model xseg_3 --face-parser-model bisenet_resnet_34