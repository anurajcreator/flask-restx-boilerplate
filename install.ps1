$content = Get-Content -Path temp_file


Set-Location $content

python -m pip install virtualenv

python -m virtualenv venv

./venv/Scripts/activate.ps1

python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt


Remove-Item temp_file

Remove-Item install.ps1


