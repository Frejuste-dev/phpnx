#!/usr/bin/env python3
"""
PHPNX WebSocket Server - Interface temps réel pour le dashboard
"""

import asyncio
import websockets
import json
import psutil
import time
from datetime import datetime
from pathlib import Path

class PHPNXWebSocketServer:
    def __init__(self, phpnx_instance):
        self.phpnx = phpnx_instance
        self.clients = set()
        self.start_time = time.time()
        self.request_count = 0
        
    async def register_client(self, websocket):
        """Enregistrer un nouveau client"""
        self.clients.add(websocket)
        print(f"🔗 Nouveau client connecté: {websocket.remote_address}")
        
    async def unregister_client(self, websocket):
        """Désenregistrer un client"""
        self.clients.discard(websocket)
        print(f"❌ Client déconnecté: {websocket.remote_address}")
        
    async def broadcast_status(self):
        """Diffuser le statut à tous les clients connectés"""
        if not self.clients:
            return
            
        status_data = await self.get_status_data()
        message = json.dumps(status_data)
        
        # Envoyer à tous les clients connectés
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
                
        # Nettoyer les clients déconnectés
        for client in disconnected_clients:
            self.clients.discard(client)
            
    async def get_status_data(self):
        """Récupérer les données de statut actuelles"""
        php_running = self.phpnx.php_process and self.phpnx.php_process.poll() is None
        nginx_running = self.phpnx.nginx_process and self.phpnx.nginx_process.poll() is None
        
        # Métriques système
        uptime = int(time.time() - self.start_time)
        uptime_str = f"{uptime//3600}h {(uptime%3600)//60}m {uptime%60}s"
        
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        
        # Logs récents
        logs = self.get_recent_logs()
        
        return {
            "php": {
                "running": php_running,
                "pid": self.phpnx.php_process.pid if php_running else None,
                "port": self.phpnx.php_port
            },
            "nginx": {
                "running": nginx_running,
                "pid": self.phpnx.nginx_process.pid if nginx_running else None,
                "port": self.phpnx.nginx_port
            },
            "metrics": {
                "uptime": uptime_str,
                "requests": self.request_count,
                "memory": f"{memory_usage:.1f}%",
                "cpu": f"{cpu_usage:.1f}%"
            },
            "logs": logs
        }
        
    def get_recent_logs(self, lines=20):
        """Récupérer les logs récents"""
        try:
            if self.phpnx.log_file.exists():
                with open(self.phpnx.log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    return [line.strip() for line in all_lines[-lines:]]
            return ["Aucun log disponible"]
        except Exception as e:
            return [f"Erreur lecture logs: {e}"]
            
    async def handle_client_message(self, websocket, message):
        """Traiter les messages des clients"""
        try:
            data = json.loads(message)
            action = data.get('action')
            
            if action == 'start':
                success = self.phpnx.start_servers()
                await websocket.send(json.dumps({
                    "type": "response",
                    "action": "start",
                    "success": success
                }))
            elif action == 'stop':
                self.phpnx.stop_servers()
                await websocket.send(json.dumps({
                    "type": "response", 
                    "action": "stop",
                    "success": True
                }))
            elif action == 'restart':
                success = self.phpnx.restart_servers()
                await websocket.send(json.dumps({
                    "type": "response",
                    "action": "restart", 
                    "success": success
                }))
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Format de message invalide"
            }))
        except Exception as e:
            await websocket.send(json.dumps({
                "type": "error",
                "message": str(e)
            }))
            
    async def handle_client(self, websocket, path):
        """Gérer une connexion client"""
        await self.register_client(websocket)
        try:
            # Envoyer le statut initial
            await self.broadcast_status()
            
            # Écouter les messages du client
            async for message in websocket:
                await self.handle_client_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
            
    async def status_broadcaster(self):
        """Diffuser le statut périodiquement"""
        while True:
            await self.broadcast_status()
            await asyncio.sleep(2)  # Mise à jour toutes les 2 secondes
            
    async def start_server(self, host='localhost', port=8765):
        """Démarrer le serveur WebSocket"""
        print(f"🚀 Démarrage du serveur WebSocket sur ws://{host}:{port}")
        
        # Démarrer le serveur WebSocket
        server = await websockets.serve(self.handle_client, host, port)
        
        # Démarrer la diffusion périodique du statut
        asyncio.create_task(self.status_broadcaster())
        
        print(f"✅ Serveur WebSocket démarré")
        return server

async def main():
    """Fonction principale pour tester le serveur WebSocket"""
    from phpnx import PHPNX
    
    phpnx = PHPNX()
    ws_server = PHPNXWebSocketServer(phpnx)
    
    server = await ws_server.start_server()
    
    try:
        await server.wait_closed()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur WebSocket...")
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())