@echo off
REM PHPNX - Le Phoenix s'élève !
REM Lanceur Windows pour PHPNX

title PHPNX - Phoenix Server Launcher
color 0E

echo.
echo     🔥 PHPNX - Le Phoenix s'élève ! 🔥
echo     ═══════════════════════════════════
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou non trouvé dans le PATH
    echo 📥 Téléchargez Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Aller dans le dossier du script
cd /d "%~dp0"

REM Vérifier si l'environnement virtuel existe
if not exist ".env" (
    echo 🔧 Création de l'environnement virtuel...
    python -m venv .env
    if %errorlevel% neq 0 (
        echo ❌ Échec de la création de l'environnement virtuel
        pause
        exit /b 1
    )
)

REM Activer l'environnement virtuel
call .env\Scripts\activate.bat

REM Installer les dépendances si nécessaire
if not exist ".env\Scripts\pip.exe" (
    echo 📦 Installation des dépendances...
    pip install -r requirements.txt
)

REM Vérifier que les dépendances sont installées
python -c "import psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installation des dépendances manquantes...
    pip install psutil
)

REM Lancer PHPNX
echo 🚀 Lancement de PHPNX...
python phpnx.py %*

REM Désactiver l'environnement virtuel
deactivate

echo.
echo 👋 PHPNX terminé. Appuyez sur une touche pour fermer...
pause >nul
