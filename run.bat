set HF_HOME=%CD%\.cache\hf_download
set HF_ENDPOINT=https://hf-mirror.com
set GRADIO_TEMP_DIR=%~dp0TEMP

uv run python facefusion.py run --open-browser