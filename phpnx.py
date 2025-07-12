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

class PHPNX:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "config" / "settings.json"
        self.log_file = self.base_dir / "logs" / "phpnx.log"
        self.php_port = 9000
        self.nginx_port = 80
        self.processes = {"php": None, "nginx": None}
        
        # Créer les dossiers nécessaires
        self.create_directories()
        self.load_config()
        
    def create_directories(self):
        """Créer la structure de dossiers"""
        dirs = ["app", "nginx/conf", "nginx/logs", "php", "static/css", 
                "static/js", "config", "logs", ".env"]
        
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
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(log_entry.strip())
        
    def check_dependencies(self):
        """Vérifier que PHP et NGINX sont présents"""
        php_path = self.base_dir / "php" / "php-cgi.exe"
        nginx_path = self.base_dir / "nginx" / "nginx.exe"
        
        if not php_path.exists():
            self.log("❌ PHP non trouvé. Téléchargez PHP depuis https://www.php.net/downloads")
            return False
            
        if not nginx_path.exists():
            self.log("❌ NGINX non trouvé. Téléchargez NGINX depuis https://nginx.org/en/download.html")
            return False
            
        return True
        
    def kill_existing_processes(self):
        """Tuer les processus PHP/NGINX existants"""
        self.log("🧹 Nettoyage des anciens processus...")
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in ['php-cgi.exe', 'nginx.exe']:
                    proc.terminate()
                    self.log(f"✅ Processus {proc.info['name']} (PID: {proc.info['pid']}) terminé")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
    def start_php(self):
        """Démarrer PHP FastCGI"""
        php_path = self.base_dir / "php" / "php-cgi.exe"
        
        cmd = [
            str(php_path),
            "-b", f"127.0.0.1:{self.php_port}",
            "-c", str(self.base_dir / "php" / "php.ini")
        ]
        
        try:
            self.processes["php"] = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir / "app"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.log(f"🐍 PHP FastCGI démarré sur le port {self.php_port}")
            return True
        except Exception as e:
            self.log(f"❌ Erreur lors du démarrage de PHP: {e}")
            return False
            
    def start_nginx(self):
        """Démarrer NGINX"""
        nginx_path = self.base_dir / "nginx" / "nginx.exe"
        
        cmd = [
            str(nginx_path),
            "-c", str(self.base_dir / "nginx" / "conf" / "nginx.conf")
        ]
        
        try:
            self.processes["nginx"] = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir / "nginx"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.log(f"🌐 NGINX démarré sur le port {self.nginx_port}")
            return True
        except Exception as e:
            self.log(f"❌ Erreur lors du démarrage de NGINX: {e}")
            return False
            
    def start_servers(self):
        """Démarrer les serveurs PHP + NGINX"""
        if not self.check_dependencies():
            return False
            
        self.kill_existing_processes()
        time.sleep(2)
        
        if self.start_php() and self.start_nginx():
            self.log("🔥 Serveurs PHPNX démarrés avec succès!")
            
            # Ouvrir le navigateur
            time.sleep(1)
            webbrowser.open(f"http://localhost:{self.nginx_port}")
            return True
        else:
            self.log("❌ Échec du démarrage des serveurs")
            return False
            
    def stop_servers(self):
        """Arrêter les serveurs"""
        self.log("🛑 Arrêt des serveurs...")
        self.kill_existing_processes()
        self.log("✅ Serveurs arrêtés")
        
    def restart_servers(self):
        """Redémarrer les serveurs"""
        self.log("🔄 Redémarrage des serveurs...")
        self.stop_servers()
        time.sleep(2)
        return self.start_servers()
        
    def show_menu(self):
        """Afficher le menu interactif"""
        phoenix_art = """
    🔥 PHPNX - Le Phoenix s'élève ! 🔥
    ═══════════════════════════════════
    """
        
        while True:
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
            os.system('cls' if os.name == 'nt' else 'clear')
            
    def show_status(self):
        """Afficher le statut des serveurs"""
        print("\n📊 Statut des serveurs:")
        print("═══════════════════════")
        
        # Vérifier les ports
        php_status = self.check_port(self.php_port)
        nginx_status = self.check_port(self.nginx_port)
        
        print(f"🐍 PHP FastCGI (port {self.php_port}): {'✅ Actif' if php_status else '❌ Inactif'}")
        print(f"🌐 NGINX (port {self.nginx_port}): {'✅ Actif' if nginx_status else '❌ Inactif'}")
        
    def check_port(self, port):
        """Vérifier si un port est utilisé"""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('127.0.0.1', port))
                return result == 0
        except:
            return False

def main():
    """Fonction principale"""
    phpnx = PHPNX()
    
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
