@echo off
pip install -r requirements.txt
pyinstaller --noconfirm --onedir --windowed --icon "icon/icon-win.ico" "my_notepad_app.py"
pause