Param(
    [Parameter(Mandatory=$True,Position=1)]
    [string]$input_dir
)

Set-Location ../newprojecttest

virtualenv venv

./venv/Scripts/acticvate.ps1

python -m pip install -r .\requirements.txt

virtualenv venv