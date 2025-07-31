#!/usr/bin/env python3
"""
Plugin Backup pour PHPNX
Système de sauvegarde automatique et manuelle
"""

import os
import shutil
import zipfile
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import threading
import time

from plugin_manager import PluginInterface

class BackupPlugin(PluginInterface):
    """Plugin de sauvegarde pour PHPNX"""
    
    def __init__(self, phpnx_instance):
        super().__init__(phpnx_instance)
        self.name = "Backup"
        self.version = "1.0.0"
        self.description = "Système de sauvegarde automatique et manuelle"
        self.author = "Kei Prince Frejuste"
        
        self.backup_dir = self.phpnx.base_dir / "backups"
        self.config_file = self.backup_dir / "backup_config.json"
        self.auto_backup_thread = None
        self.auto_backup_enabled = False
        
        # Configuration par défaut
        self.config = {
            "auto_backup_enabled": False,
            "backup_interval_hours": 24,
            "max_backups": 10,
            "backup_projects": True,
            "backup_config": True,
            "backup_logs": False,
            "compression_level": 6
        }
        
    def initialize(self):
        """Initialiser le plugin"""
        print(f"🔌 Initialisation du plugin {self.name}")
        
        # Créer le dossier de sauvegarde
        self.backup_dir.mkdir(exist_ok=True)
        
        # Charger la configuration
        self.load_config()
        
        # Démarrer la sauvegarde automatique si activée
        if self.config.get("auto_backup_enabled", False):
            self.start_auto_backup()
            
    def activate(self):
        """Activer le plugin"""
        print(f"✅ Plugin {self.name} activé")
        
    def deactivate(self):
        """Désactiver le plugin"""
        print(f"🛑 Plugin {self.name} désactivé")
        self.stop_auto_backup()
        
    def load_config(self):
        """Charger la configuration du plugin"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except Exception as e:
                print(f"Erreur chargement config backup: {e}")
                
    def save_config(self):
        """Sauvegarder la configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde config backup: {e}")
            
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Retourner les éléments de menu du plugin"""
        return [
            {
                "label": "💾 Sauvegarde Manuelle",
                "command": "backup_manual",
                "description": "Créer une sauvegarde immédiate"
            },
            {
                "label": "🔄 Sauvegarde Auto",
                "command": "backup_auto_toggle",
                "description": "Activer/désactiver la sauvegarde automatique"
            },
            {
                "label": "📋 Liste Sauvegardes",
                "command": "backup_list",
                "description": "Lister toutes les sauvegardes"
            },
            {
                "label": "🗑️ Nettoyer Sauvegardes",
                "command": "backup_cleanup",
                "description": "Supprimer les anciennes sauvegardes"
            }
        ]
        
    def handle_command(self, command: str, args: List[str]) -> bool:
        """Gérer les commandes du plugin"""
        if command == "backup_manual":
            self.create_manual_backup()
            return True
        elif command == "backup_auto_toggle":
            self.toggle_auto_backup()
            return True
        elif command == "backup_list":
            self.list_backups()
            return True
        elif command == "backup_cleanup":
            self.cleanup_old_backups()
            return True
        return False
        
    def create_manual_backup(self):
        """Créer une sauvegarde manuelle"""
        print("💾 Création d'une sauvegarde manuelle...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"phpnx_manual_{timestamp}.zip"
        backup_path = self.backup_dir / backup_name
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED, 
                               compresslevel=self.config.get("compression_level", 6)) as zipf:
                
                # Sauvegarder les projets
                if self.config.get("backup_projects", True):
                    self.add_directory_to_zip(zipf, self.phpnx.base_dir / "app", "app")
                    
                    # Sauvegarder les projets additionnels si disponibles
                    projects_dir = self.phpnx.base_dir / "projects"
                    if projects_dir.exists():
                        self.add_directory_to_zip(zipf, projects_dir, "projects")
                        
                # Sauvegarder la configuration
                if self.config.get("backup_config", True):
                    config_dir = self.phpnx.base_dir / "config"
                    if config_dir.exists():
                        self.add_directory_to_zip(zipf, config_dir, "config")
                        
                # Sauvegarder les logs si demandé
                if self.config.get("backup_logs", False):
                    logs_dir = self.phpnx.base_dir / "logs"
                    if logs_dir.exists():
                        self.add_directory_to_zip(zipf, logs_dir, "logs")
                        
                # Ajouter les métadonnées de sauvegarde
                metadata = {
                    "backup_type": "manual",
                    "created_at": datetime.now().isoformat(),
                    "phpnx_version": "1.0.0",
                    "backup_plugin_version": self.version,
                    "includes": {
                        "projects": self.config.get("backup_projects", True),
                        "config": self.config.get("backup_config", True),
                        "logs": self.config.get("backup_logs", False)
                    }
                }
                
                zipf.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
                
            print(f"✅ Sauvegarde créée: {backup_name}")
            print(f"📁 Emplacement: {backup_path}")
            
            # Nettoyer les anciennes sauvegardes si nécessaire
            self.cleanup_old_backups()
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            
    def add_directory_to_zip(self, zipf, source_dir, archive_name):
        """Ajouter un dossier à l'archive ZIP"""
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                arcname = archive_name / file_path.relative_to(source_dir)
                zipf.write(file_path, arcname)
                
    def start_auto_backup(self):
        """Démarrer la sauvegarde automatique"""
        if self.auto_backup_thread and self.auto_backup_thread.is_alive():
            return
            
        self.auto_backup_enabled = True
        self.auto_backup_thread = threading.Thread(target=self.auto_backup_worker, daemon=True)
        self.auto_backup_thread.start()
        
        print(f"🔄 Sauvegarde automatique démarrée (intervalle: {self.config.get('backup_interval_hours', 24)}h)")
        
    def stop_auto_backup(self):
        """Arrêter la sauvegarde automatique"""
        self.auto_backup_enabled = False
        if self.auto_backup_thread:
            self.auto_backup_thread.join(timeout=1)
        print("🛑 Sauvegarde automatique arrêtée")
        
    def auto_backup_worker(self):
        """Worker pour la sauvegarde automatique"""
        interval_seconds = self.config.get("backup_interval_hours", 24) * 3600
        
        while self.auto_backup_enabled:
            time.sleep(interval_seconds)
            
            if self.auto_backup_enabled:
                print("🔄 Déclenchement de la sauvegarde automatique...")
                self.create_auto_backup()
                
    def create_auto_backup(self):
        """Créer une sauvegarde automatique"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"phpnx_auto_{timestamp}.zip"
        backup_path = self.backup_dir / backup_name
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED,
                               compresslevel=self.config.get("compression_level", 6)) as zipf:
                
                # Même logique que la sauvegarde manuelle
                if self.config.get("backup_projects", True):
                    self.add_directory_to_zip(zipf, self.phpnx.base_dir / "app", "app")
                    
                    projects_dir = self.phpnx.base_dir / "projects"
                    if projects_dir.exists():
                        self.add_directory_to_zip(zipf, projects_dir, "projects")
                        
                if self.config.get("backup_config", True):
                    config_dir = self.phpnx.base_dir / "config"
                    if config_dir.exists():
                        self.add_directory_to_zip(zipf, config_dir, "config")
                        
                # Métadonnées
                metadata = {
                    "backup_type": "automatic",
                    "created_at": datetime.now().isoformat(),
                    "phpnx_version": "1.0.0",
                    "backup_plugin_version": self.version
                }
                
                zipf.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
                
            print(f"✅ Sauvegarde automatique créée: {backup_name}")
            
            # Nettoyer les anciennes sauvegardes
            self.cleanup_old_backups()
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde automatique: {e}")
            
    def toggle_auto_backup(self):
        """Activer/désactiver la sauvegarde automatique"""
        if self.auto_backup_enabled:
            self.stop_auto_backup()
            self.config["auto_backup_enabled"] = False
        else:
            self.start_auto_backup()
            self.config["auto_backup_enabled"] = True
            
        self.save_config()
        
    def list_backups(self):
        """Lister toutes les sauvegardes"""
        print("\n📋 Liste des sauvegardes:")
        print("═══════════════════════════")
        
        backups = list(self.backup_dir.glob("phpnx_*.zip"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not backups:
            print("Aucune sauvegarde trouvée")
            return
            
        for backup in backups:
            stat = backup.stat()
            size_mb = stat.st_size / (1024 * 1024)
            modified = datetime.fromtimestamp(stat.st_mtime)
            
            backup_type = "Auto" if "auto" in backup.name else "Manuel"
            
            print(f"📦 {backup.name}")
            print(f"   Type: {backup_type}")
            print(f"   Taille: {size_mb:.1f} MB")
            print(f"   Créé: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            
    def cleanup_old_backups(self):
        """Nettoyer les anciennes sauvegardes"""
        max_backups = self.config.get("max_backups", 10)
        
        backups = list(self.backup_dir.glob("phpnx_*.zip"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if len(backups) > max_backups:
            old_backups = backups[max_backups:]
            
            for backup in old_backups:
                try:
                    backup.unlink()
                    print(f"🗑️ Ancienne sauvegarde supprimée: {backup.name}")
                except Exception as e:
                    print(f"❌ Erreur suppression {backup.name}: {e}")
                    
    def restore_backup(self, backup_name: str):
        """Restaurer une sauvegarde (fonctionnalité avancée)"""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            print(f"❌ Sauvegarde {backup_name} non trouvée")
            return False
            
        print(f"🔄 Restauration de {backup_name}...")
        print("⚠️  Cette fonctionnalité nécessite l'arrêt des serveurs")
        
        # TODO: Implémenter la restauration complète
        print("🚧 Fonctionnalité de restauration en développement")
        
        return False