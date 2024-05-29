if (!(Test-Path -Path "venv")) {
    Write-Output  "Creating venv for python..."
    C:\Users\syaof\AppData\Local\Programs\Python\Python310\python.exe -m venv venv
}
.\venv\Scripts\activate

Write-Output "Installing deps..."

python -V
python -m pip install --upgrade pip
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
# pip install tensorflow
python install.py



Write-Output "Install completed"
Read-Host | Out-Null ;