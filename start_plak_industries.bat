@echo off
setlocal
cd /d "%~dp0"

echo PLAK INDUSTRIES Proje Asistani baslatiliyor...
if exist ".venv\Scripts\python.exe" (
    start "PLAK INDUSTRIES Sunucu" "%~dp0.venv\Scripts\python.exe" "%~dp0run.py"
) else (
    start "PLAK INDUSTRIES Sunucu" py "%~dp0run.py"
)

timeout /t 5 /nobreak >nul
start "" "http://127.0.0.1:5000/"
endlocal
