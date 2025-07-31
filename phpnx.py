#!/usr/bin/env python3
"""
PHPNX - Le Phoenix s'élève !
Un environnement de développement PHP local, rapide, portable et élégant.
Auteur: Kei Prince Frejuste
"""

import os
import sys
import subprocess
import time
import json
import signal
import webbrowser
import psutil
from pathlib import Path
from datetime import datetime
import platform

class PHPNX:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "config" / "settings.json"
        self.log_file = self.base_dir / "logs" / "phpnx.log"
        self.php_port = 9000
        self.nginx_port = 80
        self.php_process = None
        self.nginx_process = None
        
        # Chemins vers les exécutables
        self.php_exe = self.base_dir / "php" / "php-cgi.exe"
        self.nginx_exe = self.base_dir / "nginx" / "nginx.exe"
        
        # Créer les dossiers nécessaires
        self.create_directories()
        self.load_config()
        
    def create_directories(self):
        """Créer la structure de dossiers"""
        dirs = ["app", "nginx/conf", "nginx/logs", "php", "static/css", 
                "static/js", "config", "logs"]
        
        for dir_path in dirs:
            (self.base_dir / dir_path).mkdir(parents=True, exist_ok=True)
            
    def load_config(self):
        """Charger la configuration"""
        default_config = {
            "php_port": 9000,
            "nginx_port": 80,
            "auto_open_browser": True,
            "app_name": "PHPNX - Phoenix Server",
            "author": "Kei Prince Frejuste"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.php_port = config.get("php_port", 9000)
                    self.nginx_port = config.get("nginx_port", 80)
            except Exception as e:
                self.log(f"Erreur lors du chargement de la config: {e}")
        else:
            # Créer le fichier de config par défaut
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
                
    def log(self, message):
        """Enregistrer un message dans le log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Créer le dossier logs s'il n'existe pas
        self.log_file.parent.mkdir(exist_ok=True)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(log_entry.strip())
        
    def create_nginx_config(self):
        """Créer la configuration NGINX"""
        nginx_conf_path = self.base_dir / "nginx" / "conf" / "nginx.conf"
        app_path = str(self.base_dir / "app").replace('\\', '/')
        
        nginx_config = f"""
worker_processes 1;
error_log logs/error.log;
pid logs/nginx.pid;

events {{
    worker_connections 1024;
}}

http {{
    include mime.types;
    default_type application/octet-stream;
    
    access_log logs/access.log;
    
    sendfile on;
    keepalive_timeout 65;
    
    server {{
        listen {self.nginx_port};
        server_name localhost;
        root {app_path};
        
        index index.php index.html index.htm;
        
        # Servir les fichiers statiques depuis le dossier static
        location /style.css {{
            alias {str(self.base_dir / "static" / "css" / "style.css").replace('\\', '/')};
        }}
        
        location /script.js {{
            alias {str(self.base_dir / "static" / "js" / "script.js").replace('\\', '/')};
        }}
        
        location /favicon.ico {{
            alias {str(self.base_dir / "static" / "favicon.ico").replace('\\', '/')};
        }}
        
        # Route pour phpinfo
        location /phpinfo {{
            try_files /info.php =404;
            fastcgi_pass 127.0.0.1:{self.php_port};
            fastcgi_index info.php;
            fastcgi_param SCRIPT_FILENAME $document_root/info.php;
            include fastcgi_params;
        }}
        
        # Configuration PHP
        location ~ \\.php$ {{
            try_files $uri =404;
            fastcgi_pass 127.0.0.1:{self.php_port};
            fastcgi_index index.php;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;
        }}
        
        location / {{
            try_files $uri $uri/ =404;
        }}
    }}
}}
"""
        
        with open(nginx_conf_path, 'w') as f:
            f.write(nginx_config)
            
    def kill_existing_processes(self):
        """Tuer les processus existants sur les ports utilisés"""
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                connections = proc.info['connections']
                if connections:
                    for conn in connections:
                        if conn.laddr.port in [self.php_port, self.nginx_port]:
                            self.log(f"Arrêt du processus {proc.info['name']} (PID: {proc.info['pid']})")
                            proc.terminate()
                            proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def start_php_cgi(self):
        """Démarrer PHP FastCGI"""
        if not self.php_exe.exists():
            self.log("❌ php-cgi.exe non trouvé. Veuillez installer PHP dans le dossier php/")
            return False
            
        try:
            # Commande pour démarrer PHP FastCGI
            cmd = [
                str(self.php_exe),
                "-b", f"127.0.0.1:{self.php_port}",
                "-c", str(self.base_dir / "php")
            ]
            
            self.php_process = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Attendre un peu pour vérifier que le processus démarre
            time.sleep(2)
            
            if self.php_process.poll() is None:
                self.log(f"✅ PHP FastCGI démarré sur le port {self.php_port}")
                return True
            else:
                self.log("❌ Échec du démarrage de PHP FastCGI")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur lors du démarrage de PHP: {e}")
            return False

    def start_nginx(self):
        """Démarrer NGINX"""
        if not self.nginx_exe.exists():
            self.log("❌ nginx.exe non trouvé. Veuillez installer NGINX dans le dossier nginx/")
            return False
            
        try:
            # Créer la configuration NGINX
            self.create_nginx_config()
            
            # Démarrer NGINX
            self.nginx_process = subprocess.Popen(
                [str(self.nginx_exe)],
                cwd=str(self.base_dir / "nginx"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Attendre un peu pour vérifier que le processus démarre
            time.sleep(2)
            
            if self.nginx_process.poll() is None:
                self.log(f"✅ NGINX démarré sur le port {self.nginx_port}")
                return True
            else:
                self.log("❌ Échec du démarrage de NGINX")
                return False
                
        except Exception as e:
            self.log(f"❌ Erreur lors du démarrage de NGINX: {e}")
            return False

    def start_servers(self):
        """Démarrer les serveurs PHP + NGINX"""
        self.log("🚀 Démarrage des serveurs...")
        
        # Nettoyer les anciens processus
        self.kill_existing_processes()
        
        # Démarrer PHP FastCGI
        if not self.start_php_cgi():
            return False
            
        # Démarrer NGINX
        if not self.start_nginx():
            self.stop_servers()
            return False
            
        self.log("🔥 Serveurs PHPNX démarrés avec succès!")

        # Ouvrir le navigateur
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if config.get("auto_open_browser", True):
                        time.sleep(1)
                        webbrowser.open(f"http://localhost:{self.nginx_port}")
            except:
                pass
                
        return True
            
    def stop_servers(self):
        """Arrêter les serveurs"""
        self.log("🛑 Arrêt des serveurs...")
        
        # Arrêter NGINX
        if self.nginx_process and self.nginx_process.poll() is None:
            try:
                self.nginx_process.terminate()
                self.nginx_process.wait(timeout=5)
                self.log("✅ NGINX arrêté")
            except:
                self.nginx_process.kill()
                
        # Arrêter PHP
        if self.php_process and self.php_process.poll() is None:
            try:
                self.php_process.terminate()
                self.php_process.wait(timeout=5)
                self.log("✅ PHP FastCGI arrêté")
            except:
                self.php_process.kill()
                
        # Nettoyer les processus restants
        self.kill_existing_processes()
        
    def restart_servers(self):
        """Redémarrer les serveurs"""
        self.log("🔄 Redémarrage des serveurs...")
        self.stop_servers()
        time.sleep(2)
        return self.start_servers()
        
    def show_status(self):
        """Afficher le statut des serveurs"""
        print("\n📊 Statut des serveurs:")
        print("═══════════════════════")
        
        php_running = self.php_process and self.php_process.poll() is None
        nginx_running = self.nginx_process and self.nginx_process.poll() is None
        
        print(f"🐍 PHP FastCGI: {'✅ Actif' if php_running else '❌ Inactif'}")
        print(f"🌐 NGINX: {'✅ Actif' if nginx_running else '❌ Inactif'}")
        
        if php_running:
            print(f"   Port PHP: {self.php_port}")
        if nginx_running:
            print(f"   Port NGINX: {self.nginx_port}")
            print(f"   URL: http://localhost:{self.nginx_port}")
        
    def show_menu(self):
        """Afficher le menu interactif"""
        phoenix_art = """
    🔥 PHPNX - Le Phoenix s'élève ! 🔥
    ═══════════════════════════════════
    """
        
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(phoenix_art)
                print("1. 🚀 Démarrer les serveurs")
                print("2. 🛑 Arrêter les serveurs")
                print("3. 🔄 Redémarrer les serveurs")
                print("4. 📊 Statut des serveurs")
                print("5. 🌐 Ouvrir dans le navigateur")
                print("6. 🚪 Quitter")
                print("═══════════════════════════════════")
                
                choice = input("Choisissez une option (1-6): ").strip()
                
                if choice == "1":
                    self.start_servers()
                elif choice == "2":
                    self.stop_servers()
                elif choice == "3":
                    self.restart_servers()
                elif choice == "4":
                    self.show_status()
                elif choice == "5":
                    webbrowser.open(f"http://localhost:{self.nginx_port}")
                elif choice == "6":
                    self.stop_servers()
                    print("👋 Au revoir! Le Phoenix reviendra...")
                    break
                else:
                    print("❌ Option invalide")
                    
                input("\nAppuyez sur Entrée pour continuer...")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Interruption détectée...")
            self.stop_servers()
            print("👋 Au revoir! Le Phoenix reviendra...")

def main():
    """Fonction principale"""
    phpnx = PHPNX()
    
    # Gérer l'interruption proprement
    def signal_handler(sig, frame):
        print("\n\n🛑 Interruption détectée...")
        phpnx.stop_servers()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            phpnx.start_servers()
        elif command == "stop":
            phpnx.stop_servers()
        elif command == "restart":
            phpnx.restart_servers()
        elif command == "status":
            phpnx.show_status()
        else:
            print("Commandes disponibles: start, stop, restart, status")
    else:
        # Mode interactif
        phpnx.show_menu()

if __name__ == "__main__":
    main()