$content = Get-Content -Path filename


Set-Location $content

python -m pip install virtualenv

virtualenv venv

./venv/Scripts/activate.ps1

python -m pip install -r .\requirements.txt


Remove-Item filename

Remove-Item install.ps1