#!/bin/bash
# Script d'installation PHPNX pour Unix (Linux/macOS)
# Le Phoenix s'élève sur tous les systèmes !

set -e

echo "🔥 PHPNX Unix Installer - Le Phoenix s'élève !"
echo "═══════════════════════════════════════════════"

# Variables
PHPNX_DIR="$HOME/phpnx"
PYTHON_MIN_VERSION="3.8"
INSTALL_TYPE=""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Détecter le système d'exploitation
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        log_info "Système détecté: macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        log_info "Système détecté: Linux"
        
        # Détecter la distribution Linux
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO=$ID
            log_info "Distribution: $PRETTY_NAME"
        fi
    else
        log_error "Système d'exploitation non supporté: $OSTYPE"
        exit 1
    fi
}

# Vérifier Python
check_python() {
    log_info "Vérification de Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python $PYTHON_VERSION trouvé"
        
        # Vérifier la version minimale
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            log_success "Version Python compatible"
        else
            log_error "Python $PYTHON_MIN_VERSION ou supérieur requis"
            exit 1
        fi
    else
        log_error "Python 3 non trouvé"
        install_python
    fi
}

# Installer Python selon l'OS
install_python() {
    log_info "Installation de Python..."
    
    case $OS in
        "macos")
            if command -v brew &> /dev/null; then
                brew install python3
            else
                log_error "Homebrew non installé. Installez-le depuis https://brew.sh/"
                exit 1
            fi
            ;;
        "linux")
            case $DISTRO in
                "ubuntu"|"debian")
                    sudo apt update
                    sudo apt install -y python3 python3-pip python3-venv
                    ;;
                "centos"|"rhel"|"fedora")
                    sudo yum install -y python3 python3-pip
                    ;;
                "arch")
                    sudo pacman -S --noconfirm python python-pip
                    ;;
                *)
                    log_error "Distribution Linux non supportée pour l'installation automatique"
                    log_info "Installez Python 3.8+ manuellement"
                    exit 1
                    ;;
            esac
            ;;
    esac
}

# Installer les dépendances système
install_system_deps() {
    log_info "Installation des dépendances système..."
    
    case $OS in
        "macos")
            if command -v brew &> /dev/null; then
                log_info "Installation via Homebrew..."
                brew install nginx php
            else
                log_warning "Homebrew non installé. Installation manuelle requise."
                log_info "Installez Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            fi
            ;;
        "linux")
            case $DISTRO in
                "ubuntu"|"debian")
                    log_info "Installation via APT..."
                    sudo apt update
                    sudo apt install -y nginx php php-fpm php-cli php-common php-mysql php-xml php-curl php-gd php-mbstring php-zip curl wget git
                    ;;
                "centos"|"rhel"|"fedora")
                    log_info "Installation via YUM/DNF..."
                    if command -v dnf &> /dev/null; then
                        sudo dnf install -y nginx php php-fpm php-cli php-common php-mysqlnd php-xml php-curl php-gd php-mbstring php-zip curl wget git
                    else
                        sudo yum install -y nginx php php-fpm php-cli php-common php-mysql php-xml php-curl php-gd php-mbstring php-zip curl wget git
                    fi
                    ;;
                "arch")
                    log_info "Installation via Pacman..."
                    sudo pacman -S --noconfirm nginx php php-fpm curl wget git
                    ;;
                *)
                    log_warning "Distribution non supportée pour l'installation automatique"
                    ;;
            esac
            ;;
    esac
}

# Créer le dossier PHPNX
create_phpnx_directory() {
    log_info "Création du dossier PHPNX..."
    
    if [ -d "$PHPNX_DIR" ]; then
        log_warning "Le dossier $PHPNX_DIR existe déjà"
        read -p "Voulez-vous le supprimer et recommencer ? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$PHPNX_DIR"
            log_success "Dossier supprimé"
        else
            log_error "Installation annulée"
            exit 1
        fi
    fi
    
    mkdir -p "$PHPNX_DIR"
    cd "$PHPNX_DIR"
    log_success "Dossier PHPNX créé: $PHPNX_DIR"
}

# Télécharger PHPNX
download_phpnx() {
    log_info "Téléchargement de PHPNX..."
    
    # Si Git est disponible, cloner le repo
    if command -v git &> /dev/null; then
        git clone https://github.com/Frejuste-dev/phpnx.git .
        log_success "PHPNX téléchargé via Git"
    else
        # Sinon, télécharger l'archive ZIP
        log_info "Git non disponible, téléchargement de l'archive..."
        curl -L -o phpnx.zip https://github.com/Frejuste-dev/phpnx/archive/main.zip
        unzip phpnx.zip
        mv phpnx-main/* .
        rm -rf phpnx-main phpnx.zip
        log_success "PHPNX téléchargé via archive"
    fi
}

# Configurer l'environnement Python
setup_python_env() {
    log_info "Configuration de l'environnement Python..."
    
    # Créer l'environnement virtuel
    python3 -m venv .env
    source .env/bin/activate
    
    # Mettre à jour pip
    pip install --upgrade pip
    
    # Installer les dépendances
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Dépendances Python installées"
    else
        log_warning "Fichier requirements.txt non trouvé"
    fi
}

# Créer les scripts de lancement
create_launch_scripts() {
    log_info "Création des scripts de lancement..."
    
    # Script de lancement principal
    cat > phpnx_unix.sh << 'EOF'
#!/bin/bash
# PHPNX Unix Launcher

PHPNX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PHPNX_DIR"

# Activer l'environnement virtuel
source .env/bin/activate

# Lancer PHPNX Unix
python3 cross_platform/phpnx_unix.py "$@"
EOF

    chmod +x phpnx_unix.sh
    
    # Script GUI (si tkinter disponible)
    cat > phpnx_gui.sh << 'EOF'
#!/bin/bash
# PHPNX GUI Launcher

PHPNX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PHPNX_DIR"

# Vérifier si l'environnement graphique est disponible
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
    echo "❌ Environnement graphique non détecté"
    echo "💡 Utilisez phpnx_unix.sh pour la version CLI"
    exit 1
fi

# Activer l'environnement virtuel
source .env/bin/activate

# Lancer l'interface graphique
python3 gui/phpnx_gui.py "$@"
EOF

    chmod +x phpnx_gui.sh
    
    log_success "Scripts de lancement créés"
}

# Configurer les alias et PATH
setup_system_integration() {
    log_info "Configuration de l'intégration système..."
    
    # Ajouter au PATH via .bashrc ou .zshrc
    SHELL_RC=""
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi
    
    if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
        # Vérifier si l'alias existe déjà
        if ! grep -q "alias phpnx=" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"
            echo "# PHPNX Aliases" >> "$SHELL_RC"
            echo "alias phpnx='$PHPNX_DIR/phpnx_unix.sh'" >> "$SHELL_RC"
            echo "alias phpnx-gui='$PHPNX_DIR/phpnx_gui.sh'" >> "$SHELL_RC"
            echo "export PATH=\"$PHPNX_DIR:\$PATH\"" >> "$SHELL_RC"
            
            log_success "Aliases ajoutés à $SHELL_RC"
            log_info "Redémarrez votre terminal ou exécutez: source $SHELL_RC"
        else
            log_info "Aliases déjà configurés"
        fi
    fi
    
    # Créer un lien symbolique dans /usr/local/bin (si possible)
    if [ -w "/usr/local/bin" ]; then
        ln -sf "$PHPNX_DIR/phpnx_unix.sh" "/usr/local/bin/phpnx"
        log_success "Lien symbolique créé dans /usr/local/bin"
    fi
}

# Créer un service systemd (Linux uniquement)
create_systemd_service() {
    if [ "$OS" != "linux" ]; then
        return
    fi
    
    log_info "Création du service systemd (optionnel)..."
    
    read -p "Voulez-vous créer un service systemd pour PHPNX ? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        SERVICE_FILE="$HOME/.config/systemd/user/phpnx.service"
        mkdir -p "$(dirname "$SERVICE_FILE")"
        
        cat > "$SERVICE_FILE" << EOF
[Unit]
Description=PHPNX - Phoenix Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PHPNX_DIR
ExecStart=$PHPNX_DIR/phpnx_unix.sh start
ExecStop=$PHPNX_DIR/phpnx_unix.sh stop
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

        # Activer le service utilisateur
        systemctl --user daemon-reload
        systemctl --user enable phpnx.service
        
        log_success "Service systemd créé et activé"
        log_info "Commandes utiles:"
        log_info "  systemctl --user start phpnx    # Démarrer"
        log_info "  systemctl --user stop phpnx     # Arrêter"
        log_info "  systemctl --user status phpnx   # Statut"
    fi
}

# Test de l'installation
test_installation() {
    log_info "Test de l'installation..."
    
    # Tester le script principal
    if ./phpnx_unix.sh status; then
        log_success "Script principal fonctionnel"
    else
        log_warning "Problème avec le script principal"
    fi
    
    # Tester l'environnement Python
    source .env/bin/activate
    if python3 -c "import psutil, json, pathlib"; then
        log_success "Environnement Python fonctionnel"
    else
        log_warning "Problème avec l'environnement Python"
    fi
}

# Afficher les informations finales
show_final_info() {
    log_success "Installation PHPNX terminée !"
    echo ""
    echo "🔥 PHPNX est maintenant installé dans: $PHPNX_DIR"
    echo ""
    echo "🚀 Commandes disponibles:"
    echo "  $PHPNX_DIR/phpnx_unix.sh start     # Démarrer les serveurs"
    echo "  $PHPNX_DIR/phpnx_unix.sh stop      # Arrêter les serveurs"
    echo "  $PHPNX_DIR/phpnx_unix.sh status    # Voir le statut"
    echo "  $PHPNX_DIR/phpnx_gui.sh            # Interface graphique"
    echo ""
    
    if [ -n "$SHELL_RC" ]; then
        echo "💡 Après redémarrage du terminal, vous pourrez utiliser:"
        echo "  phpnx start                       # Démarrer"
        echo "  phpnx-gui                         # Interface graphique"
        echo ""
    fi
    
    echo "🌐 Une fois démarré, accédez à:"
    echo "  http://localhost:8080             # Site principal"
    echo "  http://admin.localhost:8080       # Dashboard"
    echo ""
    echo "📚 Documentation: https://github.com/Frejuste-dev/phpnx"
    echo "🐛 Support: https://github.com/Frejuste-dev/phpnx/issues"
    echo ""
    echo "🔥 Le Phoenix s'élève sur Unix ! 🔥"
}

# Menu d'installation
show_install_menu() {
    echo ""
    echo "Choisissez le type d'installation:"
    echo "1) Installation complète (recommandée)"
    echo "2) Installation minimale (PHPNX seulement)"
    echo "3) Installation développeur (avec outils)"
    echo "4) Quitter"
    echo ""
    
    read -p "Votre choix (1-4): " -n 1 -r
    echo ""
    
    case $REPLY in
        1)
            INSTALL_TYPE="complete"
            ;;
        2)
            INSTALL_TYPE="minimal"
            ;;
        3)
            INSTALL_TYPE="developer"
            ;;
        4)
            log_info "Installation annulée"
            exit 0
            ;;
        *)
            log_error "Choix invalide"
            show_install_menu
            ;;
    esac
}

# Installation principale
main() {
    echo ""
    log_info "Bienvenue dans l'installateur PHPNX Unix !"
    
    # Détecter l'OS
    detect_os
    
    # Menu d'installation
    show_install_menu
    
    # Vérifications préalables
    check_python
    
    # Installation des dépendances système
    if [ "$INSTALL_TYPE" != "minimal" ]; then
        install_system_deps
    fi
    
    # Création du dossier et téléchargement
    create_phpnx_directory
    download_phpnx
    
    # Configuration Python
    setup_python_env
    
    # Scripts de lancement
    create_launch_scripts
    
    # Intégration système
    if [ "$INSTALL_TYPE" != "minimal" ]; then
        setup_system_integration
        
        if [ "$INSTALL_TYPE" == "complete" ]; then
            create_systemd_service
        fi
    fi
    
    # Test de l'installation
    test_installation
    
    # Informations finales
    show_final_info
}

# Gestion des erreurs
trap 'log_error "Installation interrompue"; exit 1' INT TERM

# Lancement
main "$@"