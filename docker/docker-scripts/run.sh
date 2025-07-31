#!/bin/bash
# Script de lancement Docker pour PHPNX

set -e

echo "🔥 PHPNX Docker Run - Le Phoenix s'élève !"
echo "═══════════════════════════════════════"

# Variables
CONTAINER_NAME="phpnx-server"
IMAGE_NAME="phpnx:latest"
HTTP_PORT="80"
WEBSOCKET_PORT="8765"

# Vérifier si le conteneur existe déjà
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🔄 Arrêt et suppression du conteneur existant..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

# Créer les volumes locaux si nécessaire
echo "📁 Préparation des volumes..."
mkdir -p ../logs ../backups

# Lancer le nouveau conteneur
echo "🚀 Lancement du conteneur PHPNX..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${HTTP_PORT}:80 \
    -p ${WEBSOCKET_PORT}:8765 \
    -v "$(pwd)/../app:/opt/phpnx/app" \
    -v "$(pwd)/../projects:/opt/phpnx/projects" \
    -v "$(pwd)/../config:/opt/phpnx/config" \
    -v "$(pwd)/../logs:/opt/phpnx/logs" \
    -v "$(pwd)/../ssl:/opt/phpnx/ssl" \
    -v "$(pwd)/../plugins:/opt/phpnx/plugins" \
    -e PHPNX_VERSION=1.0.0 \
    -e TZ=Europe/Paris \
    --restart unless-stopped \
    ${IMAGE_NAME}

# Vérifier le démarrage
echo "⏳ Vérification du démarrage..."
sleep 5

if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "✅ PHPNX démarré avec succès !"
    echo ""
    echo "🌐 Accès web: http://localhost:${HTTP_PORT}"
    echo "📊 Dashboard: http://admin.localhost:${HTTP_PORT}"
    echo "📋 PHP Info: http://localhost:${HTTP_PORT}/phpinfo"
    echo "🔌 WebSocket: ws://localhost:${WEBSOCKET_PORT}"
    echo ""
    echo "📜 Logs en temps réel:"
    echo "   docker logs -f ${CONTAINER_NAME}"
    echo ""
    echo "🛑 Pour arrêter:"
    echo "   docker stop ${CONTAINER_NAME}"
    
    # Afficher les logs pendant quelques secondes
    echo "📜 Logs de démarrage:"
    docker logs ${CONTAINER_NAME}
    
else
    echo "❌ Échec du démarrage du conteneur"
    echo "📜 Logs d'erreur:"
    docker logs ${CONTAINER_NAME}
    exit 1
fi