#!/usr/bin/env python3
"""
PHPNX Enhanced - Version évoluée avec support WebSocket et fonctionnalités avancées
"""

import os
import sys
import subprocess
import time
import json
import signal
import webbrowser
import psutil
import asyncio
import threading
from pathlib import Path
from datetime import datetime
import platform
from phpnx_websocket import PHPNXWebSocketServer

class PHPNXEnhanced:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "config" / "settings.json"
        self.log_file = self.base_dir / "logs" / "phpnx.log"
        self.projects_file = self.base_dir / "config" / "projects.json"
        
        # Configuration par défaut
        self.php_port = 9000
        self.nginx_port = 80
        self.websocket_port = 8765
        self.php_process = None
        self.nginx_process = None
        self.websocket_server = None
        
        # Multi-projets
        self.current_project = "default"
        self.projects = {}
        
        # Chemins vers les exécutables
        self.php_exe = self.base_dir / "php" / "php-cgi.exe"
        self.nginx_exe = self.base_dir / "nginx" / "nginx.exe"
        
        # Créer les dossiers nécessaires
        self.create_directories()
        self.load_config()
        self.load_projects()
        
    def create_directories(self):
        """Créer la structure de dossiers étendue"""
        dirs = [
            "app", "nginx/conf", "nginx/logs", "php", 
            "static/css", "static/js", "static/admin",
            "config", "logs", "projects", "backups",
            "ssl", "plugins"
        ]
        
        for dir_path in dirs:
            (self.base_dir / dir_path).mkdir(parents=True, exist_ok=True)
            
    def load_projects(self):
        """Charger la configuration des projets"""
        default_projects = {
            "default": {
                "name": "Projet par défaut",
                "path": "app",
                "domain": "localhost",
                "php_version": "8.0",
                "ssl": False,
                "active": True
            }
        }
        
        if self.projects_file.exists():
            try:
                with open(self.projects_file, 'r', encoding='utf-8') as f:
                    self.projects = json.load(f)
            except Exception as e:
                self.log(f"Erreur lors du chargement des projets: {e}")
                self.projects = default_projects
        else:
            self.projects = default_projects
            self.save_projects()
            
    def save_projects(self):
        """Sauvegarder la configuration des projets"""
        try:
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                json.dump(self.projects, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.log(f"Erreur lors de la sauvegarde des projets: {e}")
            
    def add_project(self, project_id, name, path, domain="localhost"):
        """Ajouter un nouveau projet"""
        self.projects[project_id] = {
            "name": name,
            "path": path,
            "domain": domain,
            "php_version": "8.0",
            "ssl": False,
            "active": True,
            "created": datetime.now().isoformat()
        }
        self.save_projects()
        
        # Créer le dossier du projet
        project_path = self.base_dir / "projects" / path
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Créer un index.php par défaut
        index_file = project_path / "index.php"
        if not index_file.exists():
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(f"""<?php
echo "<h1>🔥 Projet {name}</h1>";
echo "<p>Bienvenue dans votre nouveau projet PHPNX !</p>";
echo "<p>Chemin: {path}</p>";
echo "<p>Domaine: {domain}</p>";
phpinfo();
?>""")
        
        self.log(f"✅ Projet '{name}' ajouté avec succès")
        
    def create_nginx_config_multi_projects(self):
        """Créer une configuration NGINX multi-projets"""
        nginx_conf_path = self.base_dir / "nginx" / "conf" / "nginx.conf"
        
        # Configuration de base
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
    
    # Configuration pour les fichiers statiques globaux
    server {{
        listen {self.nginx_port};
        server_name admin.localhost;
        root {str(self.base_dir / "static").replace('\\', '/')};
        
        location / {{
            try_files $uri $uri/ /admin/dashboard.html;
        }}
        
        location /api/ {{
            proxy_pass http://127.0.0.1:8765;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }}
    }}
"""
        
        # Ajouter chaque projet actif
        for project_id, project in self.projects.items():
            if not project.get('active', True):
                continue
                
            project_path = str(self.base_dir / "projects" / project['path']).replace('\\', '/')
            domain = project.get('domain', 'localhost')
            
            # Si c'est le projet par défaut, utiliser aussi localhost
            server_names = [domain]
            if project_id == 'default':
                server_names.append('localhost')
                project_path = str(self.base_dir / "app").replace('\\', '/')
                
            nginx_config += f"""
    
    # Projet: {project['name']}
    server {{
        listen {self.nginx_port};
        server_name {' '.join(server_names)};
        root {project_path};
        
        index index.php index.html index.htm;
        
        # Fichiers statiques
        location ~* \\.(css|js|png|jpg|jpeg|gif|ico|svg)$ {{
            expires 1y;
            add_header Cache-Control "public, immutable";
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
    }}"""
        
        nginx_config += "\n}\n"
        
        with open(nginx_conf_path, 'w', encoding='utf-8') as f:
            f.write(nginx_config)
            
    def start_websocket_server(self):
        """Démarrer le serveur WebSocket en arrière-plan"""
        def run_websocket():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            ws_server = PHPNXWebSocketServer(self)
            
            async def start_ws():
                server = await ws_server.start_server('localhost', self.websocket_port)
                await server.wait_closed()
                
            try:
                loop.run_until_complete(start_ws())
            except Exception as e:
                self.log(f"Erreur WebSocket: {e}")
            finally:
                loop.close()
                
        ws_thread = threading.Thread(target=run_websocket, daemon=True)
        ws_thread.start()
        self.log(f"✅ Serveur WebSocket démarré sur le port {self.websocket_port}")
        
    def backup_project(self, project_id):
        """Créer une sauvegarde d'un projet"""
        if project_id not in self.projects:
            self.log(f"❌ Projet '{project_id}' non trouvé")
            return False
            
        project = self.projects[project_id]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{project_id}_{timestamp}.zip"
        backup_path = self.base_dir / "backups" / backup_name
        
        try:
            import zipfile
            
            if project_id == 'default':
                source_path = self.base_dir / "app"
            else:
                source_path = self.base_dir / "projects" / project['path']
                
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in source_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(source_path)
                        zipf.write(file_path, arcname)
                        
            self.log(f"✅ Sauvegarde créée: {backup_name}")
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
            
    def show_enhanced_menu(self):
        """Menu interactif amélioré"""
        phoenix_art = """
    🔥 PHPNX Enhanced - Le Phoenix s'élève ! 🔥
    ═══════════════════════════════════════════════
    """
        
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(phoenix_art)
                print("🚀 SERVEURS")
                print("1. Démarrer les serveurs")
                print("2. Arrêter les serveurs") 
                print("3. Redémarrer les serveurs")
                print("4. Statut des serveurs")
                print()
                print("📁 PROJETS")
                print("5. Lister les projets")
                print("6. Ajouter un projet")
                print("7. Changer de projet actif")
                print("8. Sauvegarder un projet")
                print()
                print("🌐 INTERFACE")
                print("9. Ouvrir le dashboard web")
                print("10. Ouvrir dans le navigateur")
                print()
                print("0. Quitter")
                print("═══════════════════════════════════════════════")
                
                choice = input("Choisissez une option (0-10): ").strip()
                
                if choice == "1":
                    self.start_servers()
                elif choice == "2":
                    self.stop_servers()
                elif choice == "3":
                    self.restart_servers()
                elif choice == "4":
                    self.show_status()
                elif choice == "5":
                    self.list_projects()
                elif choice == "6":
                    self.interactive_add_project()
                elif choice == "7":
                    self.interactive_switch_project()
                elif choice == "8":
                    self.interactive_backup_project()
                elif choice == "9":
                    webbrowser.open(f"http://admin.localhost:{self.nginx_port}")
                elif choice == "10":
                    webbrowser.open(f"http://localhost:{self.nginx_port}")
                elif choice == "0":
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
            
    def list_projects(self):
        """Lister tous les projets"""
        print("\n📁 Projets configurés:")
        print("═══════════════════════")
        
        for project_id, project in self.projects.items():
            status = "✅ Actif" if project.get('active', True) else "❌ Inactif"
            current = "👑 ACTUEL" if project_id == self.current_project else ""
            
            print(f"🔹 {project_id}: {project['name']} {current}")
            print(f"   Domaine: {project.get('domain', 'localhost')}")
            print(f"   Chemin: {project['path']}")
            print(f"   Statut: {status}")
            print()
            
    def interactive_add_project(self):
        """Interface interactive pour ajouter un projet"""
        print("\n➕ Ajouter un nouveau projet")
        print("═══════════════════════════════")
        
        project_id = input("ID du projet (ex: monsite): ").strip()
        if not project_id or project_id in self.projects:
            print("❌ ID invalide ou déjà existant")
            return
            
        name = input("Nom du projet: ").strip()
        if not name:
            print("❌ Nom requis")
            return
            
        path = input(f"Chemin (défaut: {project_id}): ").strip() or project_id
        domain = input("Domaine (défaut: localhost): ").strip() or "localhost"
        
        self.add_project(project_id, name, path, domain)
        
    def interactive_switch_project(self):
        """Interface pour changer de projet actif"""
        print("\n🔄 Changer de projet actif")
        print("═══════════════════════════")
        
        self.list_projects()
        project_id = input("ID du projet à activer: ").strip()
        
        if project_id in self.projects:
            self.current_project = project_id
            print(f"✅ Projet '{project_id}' activé")
        else:
            print("❌ Projet non trouvé")
            
    def interactive_backup_project(self):
        """Interface pour sauvegarder un projet"""
        print("\n💾 Sauvegarder un projet")
        print("═══════════════════════")
        
        self.list_projects()
        project_id = input("ID du projet à sauvegarder: ").strip()
        
        if project_id in self.projects:
            self.backup_project(project_id)
        else:
            print("❌ Projet non trouvé")
            
    # Hériter des méthodes de base de PHPNX
    def load_config(self):
        """Charger la configuration étendue"""
        default_config = {
            "php_port": 9000,
            "nginx_port": 80,
            "websocket_port": 8765,
            "auto_open_browser": True,
            "app_name": "PHPNX Enhanced - Phoenix Server",
            "author": "Kei Prince Frejuste",
            "dashboard_enabled": True,
            "ssl_enabled": False
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.php_port = config.get("php_port", 9000)
                    self.nginx_port = config.get("nginx_port", 80)
                    self.websocket_port = config.get("websocket_port", 8765)
            except Exception as e:
                self.log(f"Erreur lors du chargement de la config: {e}")
        else:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
                
    def log(self, message):
        """Enregistrer un message dans le log avec horodatage"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_file.parent.mkdir(exist_ok=True)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(log_entry.strip())
        
    def start_servers(self):
        """Démarrer tous les serveurs (PHP, NGINX, WebSocket)"""
        self.log("🚀 Démarrage des serveurs Enhanced...")
        
        # Utiliser la configuration multi-projets
        self.create_nginx_config_multi_projects()
        
        # Démarrer les serveurs de base
        from phpnx import PHPNX
        base_phpnx = PHPNX()
        base_phpnx.php_port = self.php_port
        base_phpnx.nginx_port = self.nginx_port
        base_phpnx.php_exe = self.php_exe
        base_phpnx.nginx_exe = self.nginx_exe
        base_phpnx.log_file = self.log_file
        
        success = base_phpnx.start_servers()
        
        if success:
            self.php_process = base_phpnx.php_process
            self.nginx_process = base_phpnx.nginx_process
            
            # Démarrer le serveur WebSocket
            self.start_websocket_server()
            
            self.log("🔥 PHPNX Enhanced démarré avec succès!")
            
            # Ouvrir le dashboard si configuré
            if self.config_file.exists():
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        if config.get("dashboard_enabled", True):
                            time.sleep(2)
                            webbrowser.open(f"http://admin.localhost:{self.nginx_port}")
                except:
                    pass
                    
        return success
        
    def stop_servers(self):
        """Arrêter tous les serveurs"""
        self.log("🛑 Arrêt des serveurs Enhanced...")
        
        # Arrêter les serveurs de base
        from phpnx import PHPNX
        base_phpnx = PHPNX()
        base_phpnx.php_process = self.php_process
        base_phpnx.nginx_process = self.nginx_process
        base_phpnx.log_file = self.log_file
        base_phpnx.stop_servers()
        
        self.php_process = None
        self.nginx_process = None
        
    def restart_servers(self):
        """Redémarrer tous les serveurs"""
        self.log("🔄 Redémarrage des serveurs Enhanced...")
        self.stop_servers()
        time.sleep(2)
        return self.start_servers()
        
    def show_status(self):
        """Afficher le statut détaillé"""
        print("\n📊 Statut PHPNX Enhanced:")
        print("═══════════════════════════")
        
        php_running = self.php_process and self.php_process.poll() is None
        nginx_running = self.nginx_process and self.nginx_process.poll() is None
        
        print(f"🐍 PHP FastCGI: {'✅ Actif' if php_running else '❌ Inactif'}")
        print(f"🌐 NGINX: {'✅ Actif' if nginx_running else '❌ Inactif'}")
        print(f"🔌 WebSocket: ✅ Actif (Port {self.websocket_port})")
        
        if nginx_running:
            print(f"   URL principale: http://localhost:{self.nginx_port}")
            print(f"   Dashboard: http://admin.localhost:{self.nginx_port}")
            
        print(f"\n📁 Projet actuel: {self.current_project}")
        if self.current_project in self.projects:
            project = self.projects[self.current_project]
            print(f"   Nom: {project['name']}")
            print(f"   Domaine: {project.get('domain', 'localhost')}")

def main():
    """Fonction principale Enhanced"""
    phpnx = PHPNXEnhanced()
    
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
        elif command == "dashboard":
            webbrowser.open(f"http://admin.localhost:{phpnx.nginx_port}")
        else:
            print("Commandes: start, stop, restart, status, dashboard")
    else:
        phpnx.show_enhanced_menu()

if __name__ == "__main__":
    main()