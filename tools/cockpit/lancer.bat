@echo off
rem Lance le cockpit et ouvre le navigateur.
chcp 65001 >nul
cd /d "%~dp0"
python server.py --ouvrir
if errorlevel 1 pause
