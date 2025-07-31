#!/usr/bin/env python3
"""
PHPNX SSL Certificate Generator
Génère des certificats SSL auto-signés pour le développement local
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

class SSLGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.ssl_dir = self.base_dir / "ssl"
        self.ssl_dir.mkdir(exist_ok=True)
        
    def check_openssl(self):
        """Vérifier si OpenSSL est disponible"""
        try:
            result = subprocess.run(['openssl', 'version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
            
    def install_openssl_windows(self):
        """Instructions pour installer OpenSSL sur Windows"""
        print("🔐 OpenSSL n'est pas installé.")
        print("📥 Téléchargez OpenSSL depuis: https://slproweb.com/products/Win32OpenSSL.html")
        print("💡 Ou utilisez Chocolatey: choco install openssl")
        return False
        
    def generate_ca_certificate(self):
        """Générer un certificat d'autorité de certification"""
        ca_key = self.ssl_dir / "ca.key"
        ca_cert = self.ssl_dir / "ca.crt"
        
        if ca_key.exists() and ca_cert.exists():
            print("✅ Certificat CA déjà existant")
            return True
            
        try:
            # Générer la clé privée CA
            subprocess.run([
                'openssl', 'genrsa', '-out', str(ca_key), '2048'
            ], check=True, capture_output=True)
            
            # Générer le certificat CA
            subprocess.run([
                'openssl', 'req', '-new', '-x509', '-days', '365',
                '-key', str(ca_key), '-out', str(ca_cert),
                '-subj', '/C=FR/ST=France/L=Paris/O=PHPNX/OU=Development/CN=PHPNX-CA'
            ], check=True, capture_output=True)
            
            print("✅ Certificat CA généré avec succès")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la génération du CA: {e}")
            return False
            
    def generate_server_certificate(self, domain="localhost"):
        """Générer un certificat serveur pour un domaine"""
        server_key = self.ssl_dir / f"{domain}.key"
        server_csr = self.ssl_dir / f"{domain}.csr"
        server_cert = self.ssl_dir / f"{domain}.crt"
        ca_key = self.ssl_dir / "ca.key"
        ca_cert = self.ssl_dir / "ca.crt"
        
        if server_cert.exists():
            print(f"✅ Certificat pour {domain} déjà existant")
            return True
            
        try:
            # Générer la clé privée du serveur
            subprocess.run([
                'openssl', 'genrsa', '-out', str(server_key), '2048'
            ], check=True, capture_output=True)
            
            # Créer le fichier de configuration pour les extensions
            config_content = f"""[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = FR
ST = France
L = Paris
O = PHPNX
OU = Development
CN = {domain}

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = {domain}
DNS.2 = *.{domain}
DNS.3 = localhost
IP.1 = 127.0.0.1
IP.2 = ::1
"""
            
            config_file = self.ssl_dir / f"{domain}.conf"
            with open(config_file, 'w') as f:
                f.write(config_content)
            
            # Générer la demande de certificat
            subprocess.run([
                'openssl', 'req', '-new', '-key', str(server_key),
                '-out', str(server_csr), '-config', str(config_file)
            ], check=True, capture_output=True)
            
            # Signer le certificat avec le CA
            subprocess.run([
                'openssl', 'x509', '-req', '-in', str(server_csr),
                '-CA', str(ca_cert), '-CAkey', str(ca_key),
                '-CAcreateserial', '-out', str(server_cert),
                '-days', '365', '-extensions', 'v3_req',
                '-extfile', str(config_file)
            ], check=True, capture_output=True)
            
            # Nettoyer les fichiers temporaires
            server_csr.unlink()
            config_file.unlink()
            
            print(f"✅ Certificat SSL généré pour {domain}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la génération du certificat: {e}")
            return False
            
    def setup_ssl_for_project(self, project_name, domain="localhost"):
        """Configurer SSL pour un projet"""
        if not self.check_openssl():
            return self.install_openssl_windows()
            
        # Générer le CA si nécessaire
        if not self.generate_ca_certificate():
            return False
            
        # Générer le certificat serveur
        if not self.generate_server_certificate(domain):
            return False
            
        # Créer la configuration SSL
        ssl_config = {
            "enabled": True,
            "domain": domain,
            "cert_file": f"ssl/{domain}.crt",
            "key_file": f"ssl/{domain}.key",
            "ca_file": "ssl/ca.crt",
            "created": datetime.now().isoformat()
        }
        
        ssl_config_file = self.ssl_dir / f"{project_name}_ssl.json"
        with open(ssl_config_file, 'w') as f:
            json.dump(ssl_config, f, indent=4)
            
        print(f"🔐 SSL configuré pour le projet {project_name}")
        print(f"📁 Certificats dans: {self.ssl_dir}")
        print(f"🌐 Accès HTTPS: https://{domain}")
        
        return True
        
    def install_ca_certificate(self):
        """Instructions pour installer le certificat CA dans le système"""
        ca_cert = self.ssl_dir / "ca.crt"
        
        if not ca_cert.exists():
            print("❌ Certificat CA non trouvé. Générez-le d'abord.")
            return False
            
        print("🔐 Pour faire confiance au certificat CA:")
        print("Windows:")
        print(f"  1. Double-cliquez sur {ca_cert}")
        print("  2. Cliquez sur 'Installer le certificat'")
        print("  3. Choisissez 'Ordinateur local'")
        print("  4. Placez dans 'Autorités de certification racines de confiance'")
        print()
        print("macOS:")
        print(f"  sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain {ca_cert}")
        print()
        print("Linux:")
        print(f"  sudo cp {ca_cert} /usr/local/share/ca-certificates/phpnx-ca.crt")
        print("  sudo update-ca-certificates")
        
        return True

def main():
    """Fonction principale pour tester le générateur SSL"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PHPNX SSL Certificate Generator')
    parser.add_argument('--domain', default='localhost', help='Domaine pour le certificat')
    parser.add_argument('--project', default='default', help='Nom du projet')
    parser.add_argument('--install-ca', action='store_true', help='Afficher les instructions d\'installation du CA')
    
    args = parser.parse_args()
    
    ssl_gen = SSLGenerator(Path.cwd())
    
    if args.install_ca:
        ssl_gen.install_ca_certificate()
    else:
        ssl_gen.setup_ssl_for_project(args.project, args.domain)

if __name__ == "__main__":
    main()