@echo off
rem Ouvre le cockpit. Le serveur tourne sans fenetre (pythonw) et ecrit dans
rem logs\server.log. S'il repond deja sur son port, seul le navigateur s'ouvre.
chcp 65001 >nul
cd /d "%~dp0"
where pythonw >nul 2>nul
if errorlevel 1 goto console
start "" pythonw server.py --ouvrir
exit /b 0

:console
echo pythonw est introuvable : le cockpit demarre dans cette fenetre.
echo Ne la fermez pas pendant un run : cela l'arreterait.
python server.py --ouvrir
if errorlevel 1 pause
