@echo off
REM PHPNX Enhanced - Le Phoenix s'élève avec plus de puissance !
REM Lanceur Windows pour PHPNX Enhanced

title PHPNX Enhanced - Phoenix Server Launcher
color 0E

echo.
echo     🔥 PHPNX Enhanced - Le Phoenix s'élève ! 🔥
echo     ═══════════════════════════════════════════════
echo     Version Enhanced avec Dashboard Web et Multi-projets
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
echo 📦 Vérification des dépendances...
pip install -r requirements.txt --quiet

REM Lancer PHPNX Enhanced
echo 🚀 Lancement de PHPNX Enhanced...
python phpnx_enhanced.py %*

REM Désactiver l'environnement virtuel
deactivate

echo.
echo 👋 PHPNX Enhanced terminé. Appuyez sur une touche pour fermer...
pause >nul