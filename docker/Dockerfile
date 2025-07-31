# PHPNX Docker - Le Phoenix s'élève dans les conteneurs !
# Image Docker pour PHPNX avec PHP, NGINX et toutes les dépendances

FROM ubuntu:22.04

# Métadonnées
LABEL maintainer="Kei Prince Frejuste <frejuste.dev56@gmail.com>"
LABEL description="PHPNX - Environnement de développement PHP portable avec NGINX"
LABEL version="1.0.0"

# Variables d'environnement
ENV DEBIAN_FRONTEND=noninteractive
ENV PHPNX_VERSION=1.0.0
ENV PHP_PORT=9000
ENV NGINX_PORT=80
ENV PYTHONUNBUFFERED=1

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    # Serveurs web
    nginx \
    php8.1-fpm \
    php8.1-cli \
    php8.1-common \
    php8.1-mysql \
    php8.1-xml \
    php8.1-xmlrpc \
    php8.1-curl \
    php8.1-gd \
    php8.1-imagick \
    php8.1-dev \
    php8.1-imap \
    php8.1-mbstring \
    php8.1-opcache \
    php8.1-soap \
    php8.1-zip \
    php8.1-intl \
    php8.1-bcmath \
    # Python et outils
    python3 \
    python3-pip \
    python3-venv \
    # Outils système
    curl \
    wget \
    unzip \
    git \
    supervisor \
    openssl \
    ca-certificates \
    # Nettoyage
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer l'utilisateur phpnx
RUN useradd -m -s /bin/bash phpnx && \
    usermod -aG www-data phpnx

# Créer la structure de dossiers PHPNX
WORKDIR /opt/phpnx
RUN mkdir -p \
    app \
    nginx/conf \
    nginx/logs \
    static/css \
    static/js \
    static/admin \
    config \
    logs \
    projects \
    backups \
    ssl \
    plugins \
    tmp \
    run

# Copier les fichiers PHPNX
COPY app/ ./app/
COPY static/ ./static/
COPY config/ ./config/
COPY plugins/ ./plugins/
COPY ssl/ ./ssl/
COPY *.py ./
COPY requirements.txt ./

# Configuration PHP-FPM pour Docker
RUN echo '[global]' > /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'pid = /opt/phpnx/run/php-fpm.pid' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'error_log = /opt/phpnx/logs/php-fpm.log' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo '' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo '[phpnx]' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'user = phpnx' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'group = phpnx' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'listen = 127.0.0.1:9000' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'pm = dynamic' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'pm.max_children = 10' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'pm.start_servers = 3' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'pm.min_spare_servers = 2' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'pm.max_spare_servers = 5' >> /etc/php/8.1/fpm/pool.d/phpnx.conf && \
    echo 'chdir = /opt/phpnx/app' >> /etc/php/8.1/fpm/pool.d/phpnx.conf

# Configuration NGINX pour Docker
RUN echo 'user phpnx;' > /etc/nginx/nginx.conf && \
    echo 'worker_processes auto;' >> /etc/nginx/nginx.conf && \
    echo 'pid /opt/phpnx/run/nginx.pid;' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo 'events {' >> /etc/nginx/nginx.conf && \
    echo '    worker_connections 1024;' >> /etc/nginx/nginx.conf && \
    echo '}' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo 'http {' >> /etc/nginx/nginx.conf && \
    echo '    include /etc/nginx/mime.types;' >> /etc/nginx/nginx.conf && \
    echo '    default_type application/octet-stream;' >> /etc/nginx/nginx.conf && \
    echo '    access_log /opt/phpnx/logs/nginx_access.log;' >> /etc/nginx/nginx.conf && \
    echo '    error_log /opt/phpnx/logs/nginx_error.log;' >> /etc/nginx/nginx.conf && \
    echo '    sendfile on;' >> /etc/nginx/nginx.conf && \
    echo '    keepalive_timeout 65;' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo '    server {' >> /etc/nginx/nginx.conf && \
    echo '        listen 80;' >> /etc/nginx/nginx.conf && \
    echo '        server_name localhost;' >> /etc/nginx/nginx.conf && \
    echo '        root /opt/phpnx/app;' >> /etc/nginx/nginx.conf && \
    echo '        index index.php index.html;' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo '        location /style.css {' >> /etc/nginx/nginx.conf && \
    echo '            alias /opt/phpnx/static/css/style.css;' >> /etc/nginx/nginx.conf && \
    echo '        }' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo '        location /script.js {' >> /etc/nginx/nginx.conf && \
    echo '            alias /opt/phpnx/static/js/script.js;' >> /etc/nginx/nginx.conf && \
    echo '        }' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo '        location /favicon.ico {' >> /etc/nginx/nginx.conf && \
    echo '            alias /opt/phpnx/static/favicon.ico;' >> /etc/nginx/nginx.conf && \
    echo '        }' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo '        location /phpinfo {' >> /etc/nginx/nginx.conf && \
    echo '            try_files /info.php =404;' >> /etc/nginx/nginx.conf && \
    echo '            fastcgi_pass 127.0.0.1:9000;' >> /etc/nginx/nginx.conf && \
    echo '            fastcgi_index info.php;' >> /etc/nginx/nginx.conf && \
    echo '            fastcgi_param SCRIPT_FILENAME $document_root/info.php;' >> /etc/nginx/nginx.conf && \
    echo '            include fastcgi_params;' >> /etc/nginx/nginx.conf && \
    echo '        }' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo '        location ~ \.php$ {' >> /etc/nginx/nginx.conf && \
    echo '            try_files $uri =404;' >> /etc/nginx/nginx.conf && \
    echo '            fastcgi_pass 127.0.0.1:9000;' >> /etc/nginx/nginx.conf && \
    echo '            fastcgi_index index.php;' >> /etc/nginx/nginx.conf && \
    echo '            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;' >> /etc/nginx/nginx.conf && \
    echo '            include fastcgi_params;' >> /etc/nginx/nginx.conf && \
    echo '        }' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo '        location / {' >> /etc/nginx/nginx.conf && \
    echo '            try_files $uri $uri/ =404;' >> /etc/nginx/nginx.conf && \
    echo '        }' >> /etc/nginx/nginx.conf && \
    echo '    }' >> /etc/nginx/nginx.conf && \
    echo '}' >> /etc/nginx/nginx.conf

# Installation des dépendances Python
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

# Configuration Supervisor pour gérer les processus
RUN echo '[supervisord]' > /etc/supervisor/conf.d/phpnx.conf && \
    echo 'nodaemon=true' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'user=root' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'logfile=/opt/phpnx/logs/supervisord.log' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'pidfile=/opt/phpnx/run/supervisord.pid' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo '' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo '[program:php-fpm]' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'command=/usr/sbin/php-fpm8.1 --nodaemonize --fpm-config /etc/php/8.1/fpm/pool.d/phpnx.conf' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'user=phpnx' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'stdout_logfile=/opt/phpnx/logs/php-fpm.log' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'stderr_logfile=/opt/phpnx/logs/php-fpm_error.log' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo '' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo '[program:nginx]' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'command=/usr/sbin/nginx -g "daemon off;"' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'user=root' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'stdout_logfile=/opt/phpnx/logs/nginx.log' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'stderr_logfile=/opt/phpnx/logs/nginx_error.log' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo '' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo '[program:phpnx-websocket]' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'command=/usr/bin/python3 /opt/phpnx/phpnx_websocket.py' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'directory=/opt/phpnx' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'user=phpnx' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'stdout_logfile=/opt/phpnx/logs/websocket.log' >> /etc/supervisor/conf.d/phpnx.conf && \
    echo 'stderr_logfile=/opt/phpnx/logs/websocket_error.log' >> /etc/supervisor/conf.d/phpnx.conf

# Script d'entrée Docker
RUN echo '#!/bin/bash' > /opt/phpnx/docker-entrypoint.sh && \
    echo 'set -e' >> /opt/phpnx/docker-entrypoint.sh && \
    echo '' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "🔥 PHPNX Docker - Le Phoenix s'\''élève dans les conteneurs !"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "═══════════════════════════════════════════════════════════════"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo '' >> /opt/phpnx/docker-entrypoint.sh && \
    echo '# Créer les dossiers de logs et run' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'mkdir -p /opt/phpnx/logs /opt/phpnx/run' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'chown -R phpnx:phpnx /opt/phpnx' >> /opt/phpnx/docker-entrypoint.sh && \
    echo '' >> /opt/phpnx/docker-entrypoint.sh && \
    echo '# Afficher les informations de démarrage' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "🐍 PHP Version: $(php --version | head -n1)"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "🌐 NGINX Version: $(nginx -v 2>&1)"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "🐍 Python Version: $(python3 --version)"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "🔥 PHPNX Version: $PHPNX_VERSION"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo ""' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "🌐 Accès web: http://localhost:$NGINX_PORT"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "📊 Dashboard: http://admin.localhost:$NGINX_PORT"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "📋 PHP Info: http://localhost:$NGINX_PORT/phpinfo"' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo ""' >> /opt/phpnx/docker-entrypoint.sh && \
    echo '' >> /opt/phpnx/docker-entrypoint.sh && \
    echo '# Démarrer Supervisor' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'echo "🚀 Démarrage des services PHPNX..."' >> /opt/phpnx/docker-entrypoint.sh && \
    echo 'exec /usr/bin/supervisord -c /etc/supervisor/conf.d/phpnx.conf' >> /opt/phpnx/docker-entrypoint.sh && \
    chmod +x /opt/phpnx/docker-entrypoint.sh

# Permissions
RUN chown -R phpnx:phpnx /opt/phpnx && \
    chmod -R 755 /opt/phpnx

# Ports exposés
EXPOSE 80 8765

# Volume pour les projets
VOLUME ["/opt/phpnx/app", "/opt/phpnx/projects", "/opt/phpnx/logs"]

# Point d'entrée
ENTRYPOINT ["/opt/phpnx/docker-entrypoint.sh"]

# Métadonnées finales
LABEL org.opencontainers.image.title="PHPNX"
LABEL org.opencontainers.image.description="Environnement de développement PHP portable avec NGINX"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Kei Prince Frejuste <frejuste.dev56@gmail.com>"
LABEL org.opencontainers.image.url="https://github.com/Frejuste-dev/phpnx"
LABEL org.opencontainers.image.source="https://github.com/Frejuste-dev/phpnx"