#!/usr/bin/env python3
"""
PHPNX GUI - Interface graphique native avec tkinter
Interface utilisateur moderne pour PHPNX
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
import json
import webbrowser
from pathlib import Path
import sys
import os

# Ajouter le dossier parent au path pour importer phpnx
sys.path.append(str(Path(__file__).parent.parent))

try:
    from phpnx_enhanced import PHPNXEnhanced
except ImportError:
    from phpnx import PHPNX as PHPNXEnhanced

class PHPNXGui:
    def __init__(self):
        self.root = tk.Tk()
        self.phpnx = PHPNXEnhanced()
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
        self.start_status_monitor()
        
    def setup_window(self):
        """Configuration de la fenêtre principale"""
        self.root.title("🔥 PHPNX - Le Phoenix s'élève !")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Icône de la fenêtre (si disponible)
        try:
            icon_path = Path(__file__).parent.parent / "static" / "favicon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
            
        # Configuration du thème
        self.root.configure(bg='#111827')
        
    def setup_styles(self):
        """Configuration des styles ttk"""
        style = ttk.Style()
        
        # Thème sombre Phoenix
        style.theme_use('clam')
        
        # Couleurs Phoenix
        phoenix_red = '#dc2626'
        phoenix_orange = '#ea580c'
        dark_bg = '#111827'
        dark_card = '#1f2937'
        light_text = '#f9fafb'
        
        # Configuration des styles
        style.configure('Phoenix.TFrame', background=dark_bg)
        style.configure('Card.TFrame', background=dark_card, relief='raised', borderwidth=1)
        style.configure('Phoenix.TLabel', background=dark_bg, foreground=light_text, font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=dark_bg, foreground=phoenix_orange, font=('Segoe UI', 16, 'bold'))
        style.configure('Phoenix.TButton', font=('Segoe UI', 10, 'bold'))
        
        # Boutons colorés
        style.configure('Start.TButton', background=phoenix_orange, foreground='white')
        style.configure('Stop.TButton', background=phoenix_red, foreground='white')
        style.configure('Restart.TButton', background='#10b981', foreground='white')
        
    def create_widgets(self):
        """Créer tous les widgets de l'interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Phoenix.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Onglets
        self.create_server_tab()
        self.create_projects_tab()
        self.create_ssl_tab()
        self.create_logs_tab()
        self.create_settings_tab()
        
    def create_header(self, parent):
        """Créer l'en-tête avec le titre et les infos"""
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Titre principal
        title_label = ttk.Label(header_frame, text="🔥 PHPNX - Le Phoenix s'élève !", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Statut global
        self.status_frame = ttk.Frame(header_frame, style='Phoenix.TFrame')
        self.status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.php_status_label = ttk.Label(self.status_frame, text="🐍 PHP: Vérification...", 
                                         style='Phoenix.TLabel')
        self.php_status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.nginx_status_label = ttk.Label(self.status_frame, text="🌐 NGINX: Vérification...", 
                                           style='Phoenix.TLabel')
        self.nginx_status_label.pack(side=tk.LEFT)
        
    def create_server_tab(self):
        """Onglet de contrôle des serveurs"""
        server_frame = ttk.Frame(self.notebook, style='Phoenix.TFrame')
        self.notebook.add(server_frame, text="🚀 Serveurs")
        
        # Contrôles principaux
        controls_frame = ttk.LabelFrame(server_frame, text="Contrôles Serveur", 
                                       style='Phoenix.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        button_frame = ttk.Frame(controls_frame, style='Phoenix.TFrame')
        button_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="🚀 Démarrer", 
                                   command=self.start_servers, style='Start.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="🛑 Arrêter", 
                                  command=self.stop_servers, style='Stop.TButton')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.restart_btn = ttk.Button(button_frame, text="🔄 Redémarrer", 
                                     command=self.restart_servers, style='Restart.TButton')
        self.restart_btn.pack(side=tk.LEFT, padx=5)
        
        # Actions rapides
        actions_frame = ttk.LabelFrame(server_frame, text="Actions Rapides", 
                                      style='Phoenix.TFrame')
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        actions_button_frame = ttk.Frame(actions_frame, style='Phoenix.TFrame')
        actions_button_frame.pack(pady=10)
        
        ttk.Button(actions_button_frame, text="🌐 Ouvrir Site", 
                  command=self.open_website).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_button_frame, text="📊 Dashboard", 
                  command=self.open_dashboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_button_frame, text="📋 PHP Info", 
                  command=self.open_phpinfo).pack(side=tk.LEFT, padx=5)
        
        # Informations système
        info_frame = ttk.LabelFrame(server_frame, text="Informations Système", 
                                   style='Phoenix.TFrame')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=10, 
                                                  bg='#1f2937', fg='#f9fafb',
                                                  font=('Consolas', 9))
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_projects_tab(self):
        """Onglet de gestion des projets"""
        projects_frame = ttk.Frame(self.notebook, style='Phoenix.TFrame')
        self.notebook.add(projects_frame, text="📁 Projets")
        
        # Liste des projets
        list_frame = ttk.LabelFrame(projects_frame, text="Projets Configurés", 
                                   style='Phoenix.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview pour les projets
        columns = ('ID', 'Nom', 'Domaine', 'Statut')
        self.projects_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.projects_tree.heading(col, text=col)
            self.projects_tree.column(col, width=150)
            
        self.projects_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Boutons de gestion
        project_buttons_frame = ttk.Frame(projects_frame, style='Phoenix.TFrame')
        project_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(project_buttons_frame, text="➕ Nouveau Projet", 
                  command=self.add_project_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(project_buttons_frame, text="✏️ Modifier", 
                  command=self.edit_project_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(project_buttons_frame, text="🗑️ Supprimer", 
                  command=self.delete_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(project_buttons_frame, text="💾 Sauvegarder", 
                  command=self.backup_project).pack(side=tk.LEFT, padx=5)
        
    def create_ssl_tab(self):
        """Onglet de gestion SSL"""
        ssl_frame = ttk.Frame(self.notebook, style='Phoenix.TFrame')
        self.notebook.add(ssl_frame, text="🔐 SSL")
        
        # Configuration SSL
        ssl_config_frame = ttk.LabelFrame(ssl_frame, text="Configuration SSL", 
                                         style='Phoenix.TFrame')
        ssl_config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Statut SSL
        self.ssl_status_label = ttk.Label(ssl_config_frame, text="🔐 SSL: Non configuré", 
                                         style='Phoenix.TLabel')
        self.ssl_status_label.pack(pady=5)
        
        # Boutons SSL
        ssl_buttons_frame = ttk.Frame(ssl_config_frame, style='Phoenix.TFrame')
        ssl_buttons_frame.pack(pady=10)
        
        ttk.Button(ssl_buttons_frame, text="🔑 Générer Certificats", 
                  command=self.generate_ssl_certificates).pack(side=tk.LEFT, padx=5)
        ttk.Button(ssl_buttons_frame, text="📋 Installer CA", 
                  command=self.install_ca_certificate).pack(side=tk.LEFT, padx=5)
        ttk.Button(ssl_buttons_frame, text="🌐 Test HTTPS", 
                  command=self.test_https).pack(side=tk.LEFT, padx=5)
        
        # Informations SSL
        ssl_info_frame = ttk.LabelFrame(ssl_frame, text="Informations SSL", 
                                       style='Phoenix.TFrame')
        ssl_info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.ssl_info_text = scrolledtext.ScrolledText(ssl_info_frame, height=15, 
                                                      bg='#1f2937', fg='#f9fafb',
                                                      font=('Consolas', 9))
        self.ssl_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_logs_tab(self):
        """Onglet des logs"""
        logs_frame = ttk.Frame(self.notebook, style='Phoenix.TFrame')
        self.notebook.add(logs_frame, text="📜 Logs")
        
        # Contrôles des logs
        logs_controls_frame = ttk.Frame(logs_frame, style='Phoenix.TFrame')
        logs_controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(logs_controls_frame, text="🔄 Actualiser", 
                  command=self.refresh_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(logs_controls_frame, text="🗑️ Vider", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(logs_controls_frame, text="💾 Exporter", 
                  command=self.export_logs).pack(side=tk.LEFT, padx=5)
        
        # Zone d'affichage des logs
        self.logs_text = scrolledtext.ScrolledText(logs_frame, bg='#000000', fg='#00ff00',
                                                  font=('Consolas', 9))
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_settings_tab(self):
        """Onglet des paramètres"""
        settings_frame = ttk.Frame(self.notebook, style='Phoenix.TFrame')
        self.notebook.add(settings_frame, text="⚙️ Paramètres")
        
        # Configuration des ports
        ports_frame = ttk.LabelFrame(settings_frame, text="Configuration des Ports", 
                                    style='Phoenix.TFrame')
        ports_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Port PHP
        php_port_frame = ttk.Frame(ports_frame, style='Phoenix.TFrame')
        php_port_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(php_port_frame, text="Port PHP:", style='Phoenix.TLabel').pack(side=tk.LEFT)
        self.php_port_var = tk.StringVar(value=str(self.phpnx.php_port))
        ttk.Entry(php_port_frame, textvariable=self.php_port_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Port NGINX
        nginx_port_frame = ttk.Frame(ports_frame, style='Phoenix.TFrame')
        nginx_port_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(nginx_port_frame, text="Port NGINX:", style='Phoenix.TLabel').pack(side=tk.LEFT)
        self.nginx_port_var = tk.StringVar(value=str(self.phpnx.nginx_port))
        ttk.Entry(nginx_port_frame, textvariable=self.nginx_port_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Options
        options_frame = ttk.LabelFrame(settings_frame, text="Options", 
                                      style='Phoenix.TFrame')
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.auto_browser_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Ouvrir automatiquement le navigateur", 
                       variable=self.auto_browser_var, style='Phoenix.TCheckbutton').pack(anchor=tk.W, padx=5, pady=2)
        
        self.auto_start_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Démarrer automatiquement au lancement", 
                       variable=self.auto_start_var, style='Phoenix.TCheckbutton').pack(anchor=tk.W, padx=5, pady=2)
        
        # Bouton de sauvegarde
        ttk.Button(settings_frame, text="💾 Sauvegarder les Paramètres", 
                  command=self.save_settings).pack(pady=10)
        
    def start_status_monitor(self):
        """Démarrer le monitoring du statut en arrière-plan"""
        def monitor():
            while True:
                self.update_status()
                time.sleep(2)
                
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        
    def update_status(self):
        """Mettre à jour le statut des serveurs"""
        try:
            php_running = self.phpnx.php_process and self.phpnx.php_process.poll() is None
            nginx_running = self.phpnx.nginx_process and self.phpnx.nginx_process.poll() is None
            
            # Mise à jour des labels de statut
            php_status = "🐍 PHP: ✅ En ligne" if php_running else "🐍 PHP: ❌ Hors ligne"
            nginx_status = "🌐 NGINX: ✅ En ligne" if nginx_running else "🌐 NGINX: ❌ Hors ligne"
            
            self.root.after(0, lambda: self.php_status_label.config(text=php_status))
            self.root.after(0, lambda: self.nginx_status_label.config(text=nginx_status))
            
            # Mise à jour des informations système
            info_text = f"""Statut PHPNX - {time.strftime('%H:%M:%S')}
═══════════════════════════════════════

🐍 PHP FastCGI: {'✅ Actif' if php_running else '❌ Inactif'}
   Port: {self.phpnx.php_port}
   PID: {self.phpnx.php_process.pid if php_running else 'N/A'}

🌐 NGINX: {'✅ Actif' if nginx_running else '❌ Inactif'}
   Port: {self.phpnx.nginx_port}
   PID: {self.phpnx.nginx_process.pid if nginx_running else 'N/A'}

🌐 URLs:
   Site principal: http://localhost:{self.phpnx.nginx_port}
   Dashboard: http://admin.localhost:{self.phpnx.nginx_port}
   PHP Info: http://localhost:{self.phpnx.nginx_port}/phpinfo

📁 Projet actuel: {getattr(self.phpnx, 'current_project', 'default')}
"""
            
            self.root.after(0, lambda: self.update_info_text(info_text))
            
        except Exception as e:
            print(f"Erreur monitoring: {e}")
            
    def update_info_text(self, text):
        """Mettre à jour le texte d'information"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
        
    def start_servers(self):
        """Démarrer les serveurs"""
        def start():
            try:
                success = self.phpnx.start_servers()
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Succès", "🔥 Serveurs démarrés avec succès !"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Erreur", "❌ Échec du démarrage des serveurs"))
            except Exception as e:
                self.root.after(0, lambda e=e: messagebox.showerror("Erreur", f"❌ Erreur: {e}"))
                
        threading.Thread(target=start, daemon=True).start()
        
    def stop_servers(self):
        """Arrêter les serveurs"""
        def stop():
            try:
                self.phpnx.stop_servers()
                self.root.after(0, lambda: messagebox.showinfo("Succès", "🛑 Serveurs arrêtés"))
            except Exception as e:
                self.root.after(0, lambda e=e: messagebox.showerror("Erreur", f"❌ Erreur: {e}"))
                
        threading.Thread(target=stop, daemon=True).start()
        
    def restart_servers(self):
        """Redémarrer les serveurs"""
        def restart():
            try:
                success = self.phpnx.restart_servers()
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Succès", "🔄 Serveurs redémarrés avec succès !"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Erreur", "❌ Échec du redémarrage"))
            except Exception as e:
                self.root.after(0, lambda e=e: messagebox.showerror("Erreur", f"❌ Erreur: {e}"))
                
        threading.Thread(target=restart, daemon=True).start()
        
    def open_website(self):
        """Ouvrir le site web"""
        webbrowser.open(f"http://localhost:{self.phpnx.nginx_port}")
        
    def open_dashboard(self):
        """Ouvrir le dashboard"""
        webbrowser.open(f"http://admin.localhost:{self.phpnx.nginx_port}")
        
    def open_phpinfo(self):
        """Ouvrir PHP Info"""
        webbrowser.open(f"http://localhost:{self.phpnx.nginx_port}/phpinfo")
        
    def add_project_dialog(self):
        """Dialog pour ajouter un projet"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nouveau Projet")
        dialog.geometry("400x300")
        dialog.configure(bg='#111827')
        
        # Champs du formulaire
        ttk.Label(dialog, text="ID du projet:", style='Phoenix.TLabel').pack(pady=5)
        project_id_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=project_id_var).pack(pady=5)
        
        ttk.Label(dialog, text="Nom du projet:", style='Phoenix.TLabel').pack(pady=5)
        project_name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=project_name_var).pack(pady=5)
        
        ttk.Label(dialog, text="Chemin:", style='Phoenix.TLabel').pack(pady=5)
        project_path_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=project_path_var).pack(pady=5)
        
        ttk.Label(dialog, text="Domaine:", style='Phoenix.TLabel').pack(pady=5)
        project_domain_var = tk.StringVar(value="localhost")
        ttk.Entry(dialog, textvariable=project_domain_var).pack(pady=5)
        
        def create_project():
            try:
                if hasattr(self.phpnx, 'add_project'):
                    self.phpnx.add_project(
                        project_id_var.get(),
                        project_name_var.get(),
                        project_path_var.get(),
                        project_domain_var.get()
                    )
                    messagebox.showinfo("Succès", "Projet créé avec succès !")
                    dialog.destroy()
                    self.refresh_projects()
                else:
                    messagebox.showwarning("Non supporté", "Fonctionnalité non disponible dans cette version")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la création: {e}")
                
        ttk.Button(dialog, text="Créer", command=create_project).pack(pady=20)
        
    def edit_project_dialog(self):
        """Dialog pour modifier un projet"""
        messagebox.showinfo("À venir", "Fonctionnalité en développement")
        
    def delete_project(self):
        """Supprimer un projet"""
        messagebox.showinfo("À venir", "Fonctionnalité en développement")
        
    def backup_project(self):
        """Sauvegarder un projet"""
        messagebox.showinfo("À venir", "Fonctionnalité en développement")
        
    def refresh_projects(self):
        """Actualiser la liste des projets"""
        # Vider la liste actuelle
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
            
        # Recharger les projets
        if hasattr(self.phpnx, 'projects'):
            for project_id, project in self.phpnx.projects.items():
                status = "✅ Actif" if project.get('active', True) else "❌ Inactif"
                self.projects_tree.insert('', 'end', values=(
                    project_id,
                    project.get('name', 'Sans nom'),
                    project.get('domain', 'localhost'),
                    status
                ))
                
    def generate_ssl_certificates(self):
        """Générer les certificats SSL"""
        def generate():
            try:
                from ssl.generate_ssl import SSLGenerator
                ssl_gen = SSLGenerator(self.phpnx.base_dir)
                success = ssl_gen.setup_ssl_for_project('default', 'localhost')
                
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Succès", "🔐 Certificats SSL générés avec succès !"))
                    self.root.after(0, self.update_ssl_info)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Erreur", "❌ Échec de la génération SSL"))
            except Exception as e:
                self.root.after(0, lambda e=e: messagebox.showerror("Erreur", f"❌ Erreur SSL: {e}"))
                
        threading.Thread(target=generate, daemon=True).start()
        
    def install_ca_certificate(self):
        """Afficher les instructions d'installation du CA"""
        instructions = """🔐 Installation du Certificat CA

Windows:
1. Double-cliquez sur ssl/ca.crt
2. Cliquez sur 'Installer le certificat'
3. Choisissez 'Ordinateur local'
4. Placez dans 'Autorités de certification racines de confiance'

macOS:
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ssl/ca.crt

Linux:
sudo cp ssl/ca.crt /usr/local/share/ca-certificates/phpnx-ca.crt
sudo update-ca-certificates

Après installation, redémarrez votre navigateur.
"""
        messagebox.showinfo("Installation CA", instructions)
        
    def test_https(self):
        """Tester HTTPS"""
        webbrowser.open("https://localhost")
        
    def update_ssl_info(self):
        """Mettre à jour les informations SSL"""
        ssl_info = """🔐 Informations SSL PHPNX

Statut: Certificats générés
Domaine: localhost
Fichiers:
  - ssl/ca.crt (Certificat CA)
  - ssl/ca.key (Clé privée CA)
  - ssl/localhost.crt (Certificat serveur)
  - ssl/localhost.key (Clé privée serveur)

URLs HTTPS:
  - https://localhost
  - https://admin.localhost

Note: Installez le certificat CA pour éviter les avertissements de sécurité.
"""
        self.ssl_info_text.delete(1.0, tk.END)
        self.ssl_info_text.insert(1.0, ssl_info)
        
    def refresh_logs(self):
        """Actualiser les logs"""
        try:
            if self.phpnx.log_file.exists():
                with open(self.phpnx.log_file, 'r', encoding='utf-8') as f:
                    logs = f.read()
                    self.logs_text.delete(1.0, tk.END)
                    self.logs_text.insert(1.0, logs)
                    self.logs_text.see(tk.END)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lecture logs: {e}")
            
    def clear_logs(self):
        """Vider les logs"""
        if messagebox.askyesno("Confirmation", "Vider tous les logs ?"):
            try:
                with open(self.phpnx.log_file, 'w', encoding='utf-8') as f:
                    f.write("")
                self.logs_text.delete(1.0, tk.END)
                messagebox.showinfo("Succès", "Logs vidés")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {e}")
                
    def export_logs(self):
        """Exporter les logs"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Fichiers log", "*.log"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            try:
                with open(self.phpnx.log_file, 'r', encoding='utf-8') as source:
                    with open(filename, 'w', encoding='utf-8') as dest:
                        dest.write(source.read())
                messagebox.showinfo("Succès", f"Logs exportés vers {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur export: {e}")
                
    def save_settings(self):
        """Sauvegarder les paramètres"""
        try:
            # Mettre à jour les ports
            self.phpnx.php_port = int(self.php_port_var.get())
            self.phpnx.nginx_port = int(self.nginx_port_var.get())
            
            # Sauvegarder dans le fichier de config
            config = {
                "php_port": self.phpnx.php_port,
                "nginx_port": self.phpnx.nginx_port,
                "auto_open_browser": self.auto_browser_var.get(),
                "auto_start": self.auto_start_var.get(),
                "app_name": "PHPNX Enhanced - Phoenix Server",
                "author": "Kei Prince Frejuste"
            }
            
            with open(self.phpnx.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
            messagebox.showinfo("Succès", "Paramètres sauvegardés !")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur sauvegarde: {e}")
            
    def run(self):
        """Lancer l'interface graphique"""
        # Charger les projets au démarrage
        self.refresh_projects()
        self.refresh_logs()
        
        # Démarrage automatique si configuré
        if self.auto_start_var.get():
            self.root.after(1000, self.start_servers)
            
        # Lancer la boucle principale
        self.root.mainloop()

def main():
    """Fonction principale"""
    try:
        app = PHPNXGui()
        app.run()
    except Exception as e:
        print(f"Erreur lors du lancement de l'interface: {e}")
        messagebox.showerror("Erreur Critique", f"Impossible de lancer l'interface:\n{e}")

if __name__ == "__main__":
    main()