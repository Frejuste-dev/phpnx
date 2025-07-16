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
        self.nginx_port = 80
        
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
            "nginx_port": 80,
            "auto_open_browser": True,
            "app_name": "PHPNX - Phoenix Server",
            "author": "Kei Prince Frejuste"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
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
        
    def run_command(self, command):
        """Exécuter une commande shell"""
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.log(f"Erreur lors de l'exécution de la commande: {e}")
            self.log(f"Stderr: {e.stderr}")
            return None

    def start_servers(self):
        """Démarrer les serveurs PHP + NGINX"""
        self.log("🚀 Démarrage des serveurs...")
        self.run_command("sudo systemctl start php8.3-fpm")
        self.run_command("sudo systemctl start nginx")
        self.log("🔥 Serveurs PHPNX démarrés avec succès!")

        # Ouvrir le navigateur
        time.sleep(1)
        webbrowser.open(f"http://localhost:{self.nginx_port}")
        return True
            
    def stop_servers(self):
        """Arrêter les serveurs"""
        self.log("🛑 Arrêt des serveurs...")
        self.run_command("sudo systemctl stop php8.3-fpm")
        self.run_command("sudo systemctl stop nginx")
        self.log("✅ Serveurs arrêtés")
        
    def restart_servers(self):
        """Redémarrer les serveurs"""
        self.log("🔄 Redémarrage des serveurs...")
        self.run_command("sudo systemctl restart php8.3-fpm")
        self.run_command("sudo systemctl restart nginx")
        self.log("🔥 Serveurs PHPNX redémarrés avec succès!")
        return True
        
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
        
        php_status = self.run_command("systemctl is-active php8.3-fpm")
        nginx_status = self.run_command("systemctl is-active nginx")
        
        print(f"🐍 PHP-FPM: {'✅ Actif' if php_status == 'active' else '❌ Inactif'}")
        print(f"🌐 NGINX: {'✅ Actif' if nginx_status == 'active' else '❌ Inactif'}")

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
