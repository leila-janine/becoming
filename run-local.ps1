$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Test-Path '.venv\Scripts\python.exe')) {
    py -3 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.11 or 3.12 from python.org, then try again.' }
}
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependencies could not be installed.' }
$env:BECOMING_LOCAL = '1'
& '.\.venv\Scripts\python.exe' -m streamlit run app.py --server.address 127.0.0.1
