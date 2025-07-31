#!/usr/bin/env python3
"""
PHPNX Plugin Manager - Système de plugins extensible
Permet d'ajouter des fonctionnalités à PHPNX via des plugins
"""

import os
import sys
import json
import importlib
import inspect
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import traceback

class PluginInterface:
    """Interface de base pour tous les plugins PHPNX"""
    
    def __init__(self, phpnx_instance):
        self.phpnx = phpnx_instance
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.description = "Plugin PHPNX"
        self.author = "Inconnu"
        
    def initialize(self):
        """Initialiser le plugin"""
        pass
        
    def activate(self):
        """Activer le plugin"""
        pass
        
    def deactivate(self):
        """Désactiver le plugin"""
        pass
        
    def get_info(self) -> Dict[str, Any]:
        """Retourner les informations du plugin"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "active": True
        }
        
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Retourner les éléments de menu du plugin"""
        return []
        
    def handle_command(self, command: str, args: List[str]) -> bool:
        """Gérer une commande du plugin"""
        return False

class PluginManager:
    """Gestionnaire de plugins pour PHPNX"""
    
    def __init__(self, phpnx_instance):
        self.phpnx = phpnx_instance
        self.plugins_dir = Path(__file__).parent
        self.plugins: Dict[str, PluginInterface] = {}
        self.active_plugins: Dict[str, bool] = {}
        self.plugin_config_file = self.plugins_dir / "plugins_config.json"
        
        # Créer le dossier plugins s'il n'existe pas
        self.plugins_dir.mkdir(exist_ok=True)
        
        # Charger la configuration des plugins
        self.load_plugin_config()
        
    def load_plugin_config(self):
        """Charger la configuration des plugins"""
        if self.plugin_config_file.exists():
            try:
                with open(self.plugin_config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.active_plugins = config.get('active_plugins', {})
            except Exception as e:
                print(f"Erreur chargement config plugins: {e}")
                self.active_plugins = {}
        else:
            self.active_plugins = {}
            
    def save_plugin_config(self):
        """Sauvegarder la configuration des plugins"""
        try:
            config = {
                'active_plugins': self.active_plugins,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.plugin_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Erreur sauvegarde config plugins: {e}")
            
    def discover_plugins(self) -> List[str]:
        """Découvrir tous les plugins disponibles"""
        plugins = []
        
        for file_path in self.plugins_dir.glob("*.py"):
            if file_path.name.startswith("plugin_") and file_path.name != "plugin_manager.py":
                plugin_name = file_path.stem
                plugins.append(plugin_name)
                
        return plugins
        
    def load_plugin(self, plugin_name: str) -> bool:
        """Charger un plugin spécifique"""
        try:
            # Ajouter le dossier plugins au path
            if str(self.plugins_dir) not in sys.path:
                sys.path.insert(0, str(self.plugins_dir))
                
            # Importer le module du plugin
            module = importlib.import_module(plugin_name)
            
            # Trouver la classe du plugin
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, PluginInterface) and 
                    obj != PluginInterface):
                    plugin_class = obj
                    break
                    
            if plugin_class is None:
                print(f"❌ Aucune classe de plugin trouvée dans {plugin_name}")
                return False
                
            # Instancier le plugin
            plugin_instance = plugin_class(self.phpnx)
            
            # Initialiser le plugin
            plugin_instance.initialize()
            
            # Ajouter à la liste des plugins
            self.plugins[plugin_name] = plugin_instance
            
            print(f"✅ Plugin {plugin_name} chargé avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement du plugin {plugin_name}: {e}")
            traceback.print_exc()
            return False
            
    def load_all_plugins(self):
        """Charger tous les plugins disponibles"""
        plugins = self.discover_plugins()
        
        for plugin_name in plugins:
            if self.load_plugin(plugin_name):
                # Activer le plugin s'il était actif précédemment
                if self.active_plugins.get(plugin_name, True):
                    self.activate_plugin(plugin_name)
                    
    def activate_plugin(self, plugin_name: str) -> bool:
        """Activer un plugin"""
        if plugin_name not in self.plugins:
            print(f"❌ Plugin {plugin_name} non trouvé")
            return False
            
        try:
            self.plugins[plugin_name].activate()
            self.active_plugins[plugin_name] = True
            self.save_plugin_config()
            
            print(f"✅ Plugin {plugin_name} activé")
            return True
            
        except Exception as e:
            print(f"❌ Erreur activation plugin {plugin_name}: {e}")
            return False
            
    def deactivate_plugin(self, plugin_name: str) -> bool:
        """Désactiver un plugin"""
        if plugin_name not in self.plugins:
            print(f"❌ Plugin {plugin_name} non trouvé")
            return False
            
        try:
            self.plugins[plugin_name].deactivate()
            self.active_plugins[plugin_name] = False
            self.save_plugin_config()
            
            print(f"🛑 Plugin {plugin_name} désactivé")
            return True
            
        except Exception as e:
            print(f"❌ Erreur désactivation plugin {plugin_name}: {e}")
            return False
            
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Obtenir les informations d'un plugin"""
        if plugin_name in self.plugins:
            info = self.plugins[plugin_name].get_info()
            info['active'] = self.active_plugins.get(plugin_name, False)
            return info
        return None
        
    def list_plugins(self) -> List[Dict[str, Any]]:
        """Lister tous les plugins avec leurs informations"""
        plugins_info = []
        
        for plugin_name, plugin in self.plugins.items():
            info = plugin.get_info()
            info['active'] = self.active_plugins.get(plugin_name, False)
            plugins_info.append(info)
            
        return plugins_info
        
    def get_active_plugins(self) -> List[str]:
        """Obtenir la liste des plugins actifs"""
        return [name for name, active in self.active_plugins.items() if active]
        
    def handle_plugin_command(self, command: str, args: List[str]) -> bool:
        """Déléguer une commande aux plugins actifs"""
        for plugin_name in self.get_active_plugins():
            if plugin_name in self.plugins:
                if self.plugins[plugin_name].handle_command(command, args):
                    return True
        return False
        
    def get_plugin_menu_items(self) -> List[Dict[str, Any]]:
        """Obtenir tous les éléments de menu des plugins actifs"""
        menu_items = []
        
        for plugin_name in self.get_active_plugins():
            if plugin_name in self.plugins:
                items = self.plugins[plugin_name].get_menu_items()
                menu_items.extend(items)
                
        return menu_items
        
    def create_plugin_template(self, plugin_name: str, author: str = "Inconnu") -> bool:
        """Créer un template de plugin"""
        plugin_file = self.plugins_dir / f"plugin_{plugin_name.lower()}.py"
        
        if plugin_file.exists():
            print(f"❌ Le plugin {plugin_name} existe déjà")
            return False
            
        template = f'''#!/usr/bin/env python3
"""
Plugin {plugin_name} pour PHPNX
Auteur: {author}
"""

from plugin_manager import PluginInterface
from typing import Dict, List, Any

class {plugin_name.capitalize()}Plugin(PluginInterface):
    """Plugin {plugin_name} pour PHPNX"""
    
    def __init__(self, phpnx_instance):
        super().__init__(phpnx_instance)
        self.name = "{plugin_name.capitalize()}"
        self.version = "1.0.0"
        self.description = "Plugin {plugin_name} pour PHPNX"
        self.author = "{author}"
        
    def initialize(self):
        """Initialiser le plugin"""
        print(f"🔌 Initialisation du plugin {{self.name}}")
        
    def activate(self):
        """Activer le plugin"""
        print(f"✅ Plugin {{self.name}} activé")
        
    def deactivate(self):
        """Désactiver le plugin"""
        print(f"🛑 Plugin {{self.name}} désactivé")
        
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Retourner les éléments de menu du plugin"""
        return [
            {{
                "label": f"🔌 {{self.name}}",
                "command": f"{plugin_name.lower()}_action",
                "description": f"Action du plugin {{self.name}}"
            }}
        ]
        
    def handle_command(self, command: str, args: List[str]) -> bool:
        """Gérer les commandes du plugin"""
        if command == f"{plugin_name.lower()}_action":
            self.execute_action()
            return True
        return False
        
    def execute_action(self):
        """Exécuter l'action principale du plugin"""
        print(f"🚀 Exécution de l'action du plugin {{self.name}}")
        # Votre code ici
'''
        
        try:
            with open(plugin_file, 'w', encoding='utf-8') as f:
                f.write(template)
                
            print(f"✅ Template de plugin créé: {plugin_file}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création template: {e}")
            return False

def main():
    """Fonction principale pour tester le gestionnaire de plugins"""
    # Simuler une instance PHPNX
    class MockPHPNX:
        def __init__(self):
            self.base_dir = Path.cwd()
            
        def log(self, message):
            print(f"[PHPNX] {message}")
            
    phpnx = MockPHPNX()
    plugin_manager = PluginManager(phpnx)
    
    print("🔌 Gestionnaire de plugins PHPNX")
    print("═══════════════════════════════════")
    
    # Découvrir les plugins
    plugins = plugin_manager.discover_plugins()
    print(f"📦 Plugins découverts: {plugins}")
    
    # Charger tous les plugins
    plugin_manager.load_all_plugins()
    
    # Lister les plugins
    plugins_info = plugin_manager.list_plugins()
    print("\\n📋 Plugins chargés:")
    for info in plugins_info:
        status = "✅ Actif" if info['active'] else "❌ Inactif"
        print(f"  - {info['name']} v{info['version']} - {status}")
        print(f"    {info['description']} (par {info['author']})")

if __name__ == "__main__":
    main()