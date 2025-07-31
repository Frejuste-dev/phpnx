#!/usr/bin/env python3
"""
PHPNX Unix Support - Support Linux/macOS
Adaptation de PHPNX pour les systèmes Unix
"""

import os
import sys
import subprocess
import signal
import shutil
from pathlib import Path
import platform
import json
import time
import psutil
from datetime import datetime

class PHPNXUnix:
    """Version Unix de PHPNX pour Linux et macOS"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.config_file = self.base_dir / "config" / "settings.json"
        self.log_file = self.base_dir / "logs" / "phpnx.log"
        self.projects_file = self.base_dir / "config" / "projects.json"
        
        # Configuration par défaut
        self.php_port = 9000
        self.nginx_port = 8080  # Port non privilégié par défaut
        self.php_process = None
        self.nginx_process = None
        
        # Détection du système
        self.system = platform.system().lower()
        self.is_macos = self.system == "darwin"
        self.is_linux = self.system == "linux"
        
        # Chemins des exécutables
        self.detect_executables()
        
        # Créer les dossiers nécessaires
        self.create_directories()
        self.load_config()
        
    def detect_executables(self):
        """Détecter les exécutables PHP et NGINX sur le système"""
        # PHP
        self.php_exe = shutil.which("php")
        self.php_fpm_exe = shutil.which("php-fpm")
        
        # NGINX
        self.nginx_exe = shutil.which("nginx")
        
        # Vérifications
        if not self.php_exe:
            print("⚠️  PHP non trouvé dans le PATH")
            
        if not self.nginx_exe:
            print("⚠️  NGINX non trouvé dans le PATH")
            
    def create_directories(self):
        """Créer la structure de dossiers Unix"""
        dirs = [
            "app", "nginx/conf", "nginx/logs", "static/css", "static/js",
            "config", "logs", "projects", "backups", "ssl", "plugins",
            "tmp", "run"  # Dossiers spécifiques Unix
        ]
        
        for dir_path in dirs:
            (self.base_dir / dir_path).mkdir(parents=True, exist_ok=True)
            
    def load_config(self):
        """Charger la configuration Unix"""
        default_config = {
            "php_port": 9000,
            "nginx_port": 8080,  # Port non privilégié
            "auto_open_browser": True,
            "app_name": "PHPNX Unix - Phoenix Server",
            "author": "Kei Prince Frejuste",
            "use_php_fpm": True,
            "unix_socket": False
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.php_port = config.get("php_port", 9000)
                    self.nginx_port = config.get("nginx_port", 8080)
                    self.use_php_fpm = config.get("use_php_fpm", True)
            except Exception as e:
                self.log(f"Erreur chargement config: {e}")
        else:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
                
    def log(self, message):
        """Logger avec support Unix"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_file.parent.mkdir(exist_ok=True)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(log_entry.strip())
        
    def install_dependencies_macos(self):
        """Installer les dépendances sur macOS avec Homebrew"""
        print("🍺 Installation des dépendances macOS avec Homebrew...")
        
        # Vérifier si Homebrew est installé
        if not shutil.which("brew"):
            print("❌ Homebrew non installé. Installez-le depuis https://brew.sh/")
            return False
            
        try:
            # Installer PHP
            if not self.php_exe:
                subprocess.run(["brew", "install", "php"], check=True)
                
            # Installer NGINX
            if not self.nginx_exe:
                subprocess.run(["brew", "install", "nginx"], check=True)
                
            # Re-détecter les exécutables
            self.detect_executables()
            
            print("✅ Dépendances macOS installées")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur installation macOS: {e}")
            return False
            
    def install_dependencies_linux(self):
        """Installer les dépendances sur Linux"""
        print("🐧 Installation des dépendances Linux...")
        
        # Détecter le gestionnaire de paquets
        if shutil.which("apt"):
            return self.install_with_apt()
        elif shutil.which("yum"):
            return self.install_with_yum()
        elif shutil.which("pacman"):
            return self.install_with_pacman()
        else:
            print("❌ Gestionnaire de paquets non supporté")
            return False
            
    def install_with_apt(self):
        """Installation avec APT (Debian/Ubuntu)"""
        try:
            # Mettre à jour les paquets
            subprocess.run(["sudo", "apt", "update"], check=True)
            
            # Installer PHP
            if not self.php_exe:
                subprocess.run(["sudo", "apt", "install", "-y", "php", "php-fpm", "php-cli"], check=True)
                
            # Installer NGINX
            if not self.nginx_exe:
                subprocess.run(["sudo", "apt", "install", "-y", "nginx"], check=True)
                
            self.detect_executables()
            print("✅ Dépendances Linux (APT) installées")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur installation APT: {e}")
            return False
            
    def install_with_yum(self):
        """Installation avec YUM (RedHat/CentOS)"""
        try:
            # Installer PHP
            if not self.php_exe:
                subprocess.run(["sudo", "yum", "install", "-y", "php", "php-fpm"], check=True)
                
            # Installer NGINX
            if not self.nginx_exe:
                subprocess.run(["sudo", "yum", "install", "-y", "nginx"], check=True)
                
            self.detect_executables()
            print("✅ Dépendances Linux (YUM) installées")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur installation YUM: {e}")
            return False
            
    def install_with_pacman(self):
        """Installation avec Pacman (Arch Linux)"""
        try:
            # Installer PHP
            if not self.php_exe:
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "php", "php-fpm"], check=True)
                
            # Installer NGINX
            if not self.nginx_exe:
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "nginx"], check=True)
                
            self.detect_executables()
            print("✅ Dépendances Linux (Pacman) installées")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur installation Pacman: {e}")
            return False
            
    def create_nginx_config_unix(self):
        """Créer la configuration NGINX pour Unix"""
        nginx_conf_path = self.base_dir / "nginx" / "conf" / "nginx.conf"
        app_path = str(self.base_dir / "app")
        
        # Configuration NGINX adaptée pour Unix
        nginx_config = f"""
worker_processes auto;
error_log {self.base_dir}/nginx/logs/error.log;
pid {self.base_dir}/run/nginx.pid;

events {{
    worker_connections 1024;
    use epoll;
}}

http {{
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    access_log {self.base_dir}/nginx/logs/access.log;
    
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    server {{
        listen {self.nginx_port};
        server_name localhost;
        root {app_path};
        
        index index.php index.html index.htm;
        
        # Servir les fichiers statiques
        location /style.css {{
            alias {self.base_dir}/static/css/style.css;
        }}
        
        location /script.js {{
            alias {self.base_dir}/static/js/script.js;
        }}
        
        location /favicon.ico {{
            alias {self.base_dir}/static/favicon.ico;
        }}
        
        # Route pour phpinfo
        location /phpinfo {{
            try_files /info.php =404;
            fastcgi_pass 127.0.0.1:{self.php_port};
            fastcgi_index info.php;
            fastcgi_param SCRIPT_FILENAME $document_root/info.php;
            include /etc/nginx/fastcgi_params;
        }}
        
        # Configuration PHP
        location ~ \.php$ {{
            try_files $uri =404;
            fastcgi_pass 127.0.0.1:{self.php_port};
            fastcgi_index index.php;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include /etc/nginx/fastcgi_params;
        }}
        
        location / {{
            try_files $uri $uri/ =404;
        }}
    }}
}}
"""
        
        with open(nginx_conf_path, 'w', encoding='utf-8') as f:
            f.write(nginx_config)
            
    def start_php_fpm(self):
        """Démarrer PHP-FPM sur Unix"""
        if not self.php_fpm_exe:
            return self.start_php_cgi_unix()
            
        try:
            # Créer la configuration PHP-FPM
            fpm_config = self.create_php_fpm_config()
            
            # Démarrer PHP-FPM
            cmd = [
                self.php_fpm_exe,
                "--fpm-config", str(fpm_config),
                "--nodaemonize"
            ]
            
            self.php_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(2)
            
            if self.php_process.poll() is None:
                self.log(f"✅ PHP-FPM démarré sur le port {self.php_port}")
                return True
            else:
                self.log("❌ Échec du démarrage de PHP-FPM")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur PHP-FPM: {e}")
            return False
            
    def create_php_fpm_config(self):
        """Créer la configuration PHP-FPM"""
        fpm_config_path = self.base_dir / "config" / "php-fpm.conf"
        
        config_content = f"""[global]
pid = {self.base_dir}/run/php-fpm.pid
error_log = {self.base_dir}/logs/php-fpm.log

[www]
user = {os.getenv('USER', 'www-data')}
group = {os.getenv('USER', 'www-data')}

listen = 127.0.0.1:{self.php_port}
listen.owner = {os.getenv('USER', 'www-data')}
listen.group = {os.getenv('USER', 'www-data')}
listen.mode = 0660

pm = dynamic
pm.max_children = 5
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3

chdir = {self.base_dir}/app
"""
        
        with open(fmp_config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
            
        return fpm_config_path
        
    def start_php_cgi_unix(self):
        """Démarrer PHP-CGI sur Unix (fallback)"""
        if not self.php_exe:
            self.log("❌ PHP non trouvé")
            return False
            
        try:
            # Utiliser spawn-fcgi si disponible, sinon php-cgi direct
            spawn_fcgi = shutil.which("spawn-fcgi")
            
            if spawn_fcgi:
                cmd = [
                    spawn_fcgi,
                    "-a", "127.0.0.1",
                    "-p", str(self.php_port),
                    "-f", self.php_exe
                ]
            else:
                # Mode CGI direct
                env = os.environ.copy()
                env["FCGI_WEB_SERVER_ADDRS"] = "127.0.0.1"
                
                cmd = [self.php_exe, "-b", f"127.0.0.1:{self.php_port}"]
                
            self.php_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env if not spawn_fcgi else None
            )
            
            time.sleep(2)
            
            if self.php_process.poll() is None:
                self.log(f"✅ PHP-CGI démarré sur le port {self.php_port}")
                return True
            else:
                self.log("❌ Échec du démarrage de PHP-CGI")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur PHP-CGI: {e}")
            return False
            
    def start_nginx_unix(self):
        """Démarrer NGINX sur Unix"""
        if not self.nginx_exe:
            self.log("❌ NGINX non trouvé")
            return False
            
        try:
            # Créer la configuration
            self.create_nginx_config_unix()
            
            # Démarrer NGINX
            cmd = [
                self.nginx_exe,
                "-c", str(self.base_dir / "nginx" / "conf" / "nginx.conf"),
                "-g", "daemon off;"
            ]
            
            self.nginx_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(2)
            
            if self.nginx_process.poll() is None:
                self.log(f"✅ NGINX démarré sur le port {self.nginx_port}")
                return True
            else:
                self.log("❌ Échec du démarrage de NGINX")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur NGINX: {e}")
            return False
            
    def start_servers(self):
        """Démarrer les serveurs Unix"""
        self.log("🚀 Démarrage des serveurs Unix...")
        
        # Vérifier les dépendances
        if not self.php_exe or not self.nginx_exe:
            self.log("❌ Dépendances manquantes")
            
            if self.is_macos:
                if not self.install_dependencies_macos():
                    return False
            elif self.is_linux:
                if not self.install_dependencies_linux():
                    return False
                    
        # Nettoyer les anciens processus
        self.kill_existing_processes()
        
        # Démarrer PHP
        if self.use_php_fpm and self.php_fpm_exe:
            php_started = self.start_php_fpm()
        else:
            php_started = self.start_php_cgi_unix()
            
        if not php_started:
            return False
            
        # Démarrer NGINX
        if not self.start_nginx_unix():
            self.stop_servers()
            return False
            
        self.log("🔥 Serveurs Unix démarrés avec succès!")
        
        # Ouvrir le navigateur si configuré
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if config.get("auto_open_browser", True):
                        self.open_browser()
            except:
                pass
                
        return True
        
    def stop_servers(self):
        """Arrêter les serveurs Unix"""
        self.log("🛑 Arrêt des serveurs Unix...")
        
        # Arrêter NGINX
        if self.nginx_process:
            try:
                self.nginx_process.terminate()
                self.nginx_process.wait(timeout=5)
                self.log("✅ NGINX arrêté")
            except:
                self.nginx_process.kill()
                
        # Arrêter PHP
        if self.php_process:
            try:
                self.php_process.terminate()
                self.php_process.wait(timeout=5)
                self.log("✅ PHP arrêté")
            except:
                self.php_process.kill()
                
        # Nettoyer les processus restants
        self.kill_existing_processes()
        
    def kill_existing_processes(self):
        """Tuer les processus existants sur les ports utilisés"""
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                connections = proc.info['connections']
                if connections:
                    for conn in connections:
                        if hasattr(conn, 'laddr') and conn.laddr.port in [self.php_port, self.nginx_port]:
                            self.log(f"Arrêt du processus {proc.info['name']} (PID: {proc.info['pid']})")
                            proc.terminate()
                            proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
    def open_browser(self):
        """Ouvrir le navigateur sur Unix"""
        url = f"http://localhost:{self.nginx_port}"
        
        try:
            if self.is_macos:
                subprocess.run(["open", url])
            else:
                subprocess.run(["xdg-open", url])
        except:
            print(f"🌐 Ouvrez votre navigateur sur: {url}")
            
    def show_status(self):
        """Afficher le statut Unix"""
        print(f"\n📊 Statut PHPNX Unix ({self.system.title()}):")
        print("═══════════════════════════════════════")
        
        php_running = self.php_process and self.php_process.poll() is None
        nginx_running = self.nginx_process and self.nginx_process.poll() is None
        
        php_type = "PHP-FPM" if self.use_php_fpm and self.php_fpm_exe else "PHP-CGI"
        
        print(f"🐍 {php_type}: {'✅ Actif' if php_running else '❌ Inactif'}")
        print(f"🌐 NGINX: {'✅ Actif' if nginx_running else '❌ Inactif'}")
        
        if php_running:
            print(f"   Port PHP: {self.php_port}")
        if nginx_running:
            print(f"   Port NGINX: {self.nginx_port}")
            print(f"   URL: http://localhost:{self.nginx_port}")

def main():
    """Fonction principale Unix"""
    phpnx = PHPNXUnix()
    
    def signal_handler(sig, frame):
        print("\n\n🛑 Interruption détectée...")
        phpnx.stop_servers()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            phpnx.start_servers()
        elif command == "stop":
            phpnx.stop_servers()
        elif command == "restart":
            phpnx.stop_servers()
            time.sleep(2)
            phpnx.start_servers()
        elif command == "status":
            phpnx.show_status()
        elif command == "install":
            if phpnx.is_macos:
                phpnx.install_dependencies_macos()
            elif phpnx.is_linux:
                phpnx.install_dependencies_linux()
        else:
            print("Commandes: start, stop, restart, status, install")
    else:
        # Mode interactif simple
        print("🔥 PHPNX Unix - Le Phoenix s'élève sur Unix !")
        print("Commandes disponibles: start, stop, restart, status, install")

if __name__ == "__main__":
    main()