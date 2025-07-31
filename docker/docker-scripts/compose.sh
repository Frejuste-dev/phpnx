#!/bin/bash
# Script Docker Compose pour PHPNX avec différents profils

set -e

echo "🔥 PHPNX Docker Compose - Le Phoenix s'élève !"
echo "═══════════════════════════════════════════════"

# Fonction d'aide
show_help() {
    echo "Usage: $0 [COMMAND] [PROFILE]"
    echo ""
    echo "Commands:"
    echo "  up       - Démarrer les services"
    echo "  down     - Arrêter les services"
    echo "  restart  - Redémarrer les services"
    echo "  logs     - Afficher les logs"
    echo "  status   - Afficher le statut"
    echo "  build    - Construire les images"
    echo ""
    echo "Profiles disponibles:"
    echo "  basic      - PHPNX seul (défaut)"
    echo "  database   - PHPNX + MySQL + Adminer"
    echo "  postgres   - PHPNX + PostgreSQL + Adminer"
    echo "  cache      - PHPNX + Redis"
    echo "  mail       - PHPNX + Mailhog"
    echo "  full       - Tous les services"
    echo "  monitoring - PHPNX + Portainer"
    echo ""
    echo "Exemples:"
    echo "  $0 up                    # Démarrer PHPNX seul"
    echo "  $0 up database           # Démarrer PHPNX + MySQL"
    echo "  $0 up full               # Démarrer tous les services"
    echo "  $0 logs phpnx            # Voir les logs de PHPNX"
}

# Vérifier que nous sommes dans le bon dossier
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Erreur: Exécutez ce script depuis le dossier docker/"
    exit 1
fi

# Variables
COMMAND=${1:-help}
PROFILE=${2:-basic}

# Définir les profils
case $PROFILE in
    "basic")
        PROFILES=""
        ;;
    "database")
        PROFILES="--profile database"
        ;;
    "postgres")
        PROFILES="--profile database --profile postgres"
        ;;
    "cache")
        PROFILES="--profile cache"
        ;;
    "mail")
        PROFILES="--profile mail"
        ;;
    "monitoring")
        PROFILES="--profile monitoring"
        ;;
    "full")
        PROFILES="--profile database --profile cache --profile mail --profile tools --profile monitoring"
        ;;
    *)
        echo "❌ Profil inconnu: $PROFILE"
        show_help
        exit 1
        ;;
esac

# Exécuter la commande
case $COMMAND in
    "up")
        echo "🚀 Démarrage des services PHPNX (profil: $PROFILE)..."
        docker-compose $PROFILES up -d
        
        echo "⏳ Attente du démarrage des services..."
        sleep 10
        
        echo "✅ Services démarrés !"
        echo ""
        echo "🌐 PHPNX: http://localhost"
        echo "📊 Dashboard: http://admin.localhost"
        
        if [[ $PROFILES == *"database"* ]]; then
            echo "🗄️  Adminer: http://localhost:8080"
        fi
        
        if [[ $PROFILES == *"mail"* ]]; then
            echo "📧 Mailhog: http://localhost:8025"
        fi
        
        if [[ $PROFILES == *"monitoring"* ]]; then
            echo "📊 Portainer: http://localhost:9000"
        fi
        ;;
        
    "down")
        echo "🛑 Arrêt des services PHPNX..."
        docker-compose $PROFILES down
        echo "✅ Services arrêtés"
        ;;
        
    "restart")
        echo "🔄 Redémarrage des services PHPNX..."
        docker-compose $PROFILES restart
        echo "✅ Services redémarrés"
        ;;
        
    "logs")
        SERVICE=${3:-phpnx}
        echo "📜 Logs du service $SERVICE:"
        docker-compose logs -f $SERVICE
        ;;
        
    "status")
        echo "📊 Statut des services PHPNX:"
        docker-compose $PROFILES ps
        ;;
        
    "build")
        echo "🔨 Construction des images..."
        docker-compose $PROFILES build
        echo "✅ Images construites"
        ;;
        
    "help"|*)
        show_help
        ;;
esac