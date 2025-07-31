#!/bin/bash
# Script de construction Docker pour PHPNX

set -e

echo "🔥 PHPNX Docker Build - Le Phoenix s'élève !"
echo "═══════════════════════════════════════════"

# Variables
IMAGE_NAME="phpnx"
IMAGE_TAG="latest"
DOCKERFILE_PATH="docker/Dockerfile"

# Vérifier que nous sommes dans le bon dossier
if [ ! -f "phpnx.py" ]; then
    echo "❌ Erreur: Exécutez ce script depuis la racine du projet PHPNX"
    exit 1
fi

# Construire l'image
echo "🔨 Construction de l'image Docker..."
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -f "${DOCKERFILE_PATH}" .

# Vérifier la construction
if [ $? -eq 0 ]; then
    echo "✅ Image Docker construite avec succès !"
    echo "📦 Image: ${IMAGE_NAME}:${IMAGE_TAG}"
    
    # Afficher les informations de l'image
    echo ""
    echo "📊 Informations de l'image:"
    docker images "${IMAGE_NAME}:${IMAGE_TAG}"
    
    echo ""
    echo "🚀 Pour démarrer PHPNX avec Docker:"
    echo "   docker run -d -p 80:80 -p 8765:8765 --name phpnx ${IMAGE_NAME}:${IMAGE_TAG}"
    echo ""
    echo "🐙 Ou utilisez Docker Compose:"
    echo "   cd docker && docker-compose up -d"
    
else
    echo "❌ Échec de la construction de l'image Docker"
    exit 1
fi