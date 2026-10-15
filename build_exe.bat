@echo off
rem Pravi dist\DJ asistent\DJ asistent.exe (potreban Python 3.12 ili 3.13 u PATH-u)
cd /d "%~dp0"
if not exist build_env (
  python -m venv build_env || goto :err
  build_env\Scripts\python -m pip install -r requirements.txt pywebview pyinstaller || goto :err
)
build_env\Scripts\pyinstaller --noconfirm --clean --windowed --name "DJ asistent" ^
  --add-data "app\static;app\static" ^
  --collect-submodules uvicorn --hidden-import app.main ^
  desktop.py || goto :err
echo.
echo Gotovo: dist\DJ asistent\DJ asistent.exe
pause
exit /b 0
:err
echo Greska pri pravljenju.
pause
exit /b 1
