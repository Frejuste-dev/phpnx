<h1 align="center">🔥 PHPNX - Le Phoenix s’élève !</h1>

<p align="center">
    <img src="https://img.shields.io/badge/PHP-Ready-blue?style=for-the-badge&logo=php" alt="PHP Ready" />
    <img src="https://img.shields.io/badge/NGINX-Bundled-green?style=for-the-badge&logo=nginx" alt="NGINX" />
    <img src="https://img.shields.io/badge/Python-Automation-yellow?style=for-the-badge&logo=python" alt="Python Automation" />
    <img src="https://img.shields.io/badge/Windows-Portable-lightgrey?style=for-the-badge&logo=windows" alt="Windows Portable" />
</p>
<p align="center"><i>Un environnement de développement PHP local, rapide, portable et élégant. Alimenté par la puissance du Phoenix. 🐦‍🔥</i></p>

---

## ✨ Pourquoi PHPNX ?

> Parce que les développeurs méritent mieux qu’un `localhost` bricolé.  
> Parce qu’on en a marre des installations lourdes et complexes.  
> Parce qu’un outil qui allume NGINX & PHP en un clic, c’est juste... magique.

PHPNX est un launcher **portable, automatisé et stylé** basé sur **NGINX + PHP + Python** qui :
- démarre vos serveurs en un clic,
- fonctionne hors ligne,
- propose un menu interactif,
- et transforme votre projet local en un havre de productivité.

---

## 🧱 Structure du Projet

```bash
phpnx/
├── app/                    # Vos fichiers PHP
│   ├── index.php          # Page d'accueil par défaut
│   └── info.php           # Page info PHP (optionnel)
├── nginx/                 # NGINX portable (à télécharger)
│   ├── conf/
│   │   └── nginx.conf     # Configuration NGINX
│   ├── logs/              # Logs NGINX
│   └── nginx.exe          # Exécutable NGINX
├── php/                   # PHP portable (à télécharger)
│   ├── php.exe
│   ├── php-cgi.exe
│   └── php.ini
├── static/                # Assets statiques
│   ├── css/
│   │   └── style.css      # Styles pour l'interface
│   ├── js/
│   │   └── script.js      # Scripts JS
│   └── favicon.ico        # Favicon Phoenix
├── .env/                  # Environnement virtuel Python (auto-créé)
├── config/                # Configurations
│   └── settings.json      # Paramètres PHPNX
├── logs/                  # Logs du système
│   └── phpnx.log         # Log principal
├── phpnx.py              # Script Python principal
├── phpnx.bat             # Lanceur Windows
├── requirements.txt      # Dépendances Python
├── README.md            # Documentation
└── .gitignore           # Fichiers à ignorer
```


---

## 🚀 Fonctionnalités

- ✅ Zéro configuration manuelle
- 🧠 Script Python intelligent (`server.py`)
- 🛠 Interface interactive (démarrer, arrêter, redémarrer)
- 🧪 Compatible tous projets PHP
- 🎯 Installation 100% portable (clé USB, disque dur, etc.)
- 💻 Aucun serveur global requis
- 🔥 Ambiance Phoenix garantie

---

## 📸 Aperçu

<p align="center">
  <img src="https://user-images.githubusercontent.com/0000000/phpnx_demo.gif" alt="Demo Interface PHPNX" width="720" />
</p>

---

## 🛠 Installation (Windows)

1. **Cloner le repo ou télécharger le .zip**
2. Placer vos fichiers PHP dans le dossier `app/`
3. Double-cliquer sur `phpnx.bat`
4. ✨ C’est lancé. Votre serveur est prêt sur [http://localhost](http://localhost)

---

## 🐍 Dépendances

- [x] Python 3.8+
- [x] NGINX portable
- [x] PHP CGI (php-cgi.exe)

---

## 📥 Installation manuelle

1. Télécharge PHP depuis [php.net](https://www.php.net/downloads)
2. Télécharge NGINX depuis [nginx.org](https://nginx.org/en/download.html)
3. Place les deux dossiers dans `C:/phpnx/php` et `C:/phpnx/nginx`

---

## 🧪 Mode terminal (optionnel)

```bash
  python phpnx.py start    # Lancer PHP + NGINX
  python phpnx.py stop     # Stopper les serveurs
  python phpnx.py restart  # Restart propre
  python phpnx.py          # Mode menu interactif
```

---

## 🗺️ État du Projet & Feuille de Route

> Voici un aperçu clair des fonctionnalités **actuellement en place**, celles **en cours de développement**, et celles **que nous imaginons pour l'avenir**.  

### ✅ Fonctionnalités déjà codées

- [x] 📦 Environnement 100% portable (aucune installation système requise)
- [x] 🐍 Script Python `server.py` interactif (start, stop, restart)
- [x] 🧪 Menu en ligne de commande avec choix utilisateur
- [x] 🪄 Lancement automatique de PHP FastCGI + NGINX
- [x] 🌐 Ouverture du navigateur sur `http://localhost`
- [x] ⚙️ Détection et création automatique d’un environnement virtuel Python `.env`
- [x] 📁 Structure standardisée (`php/`, `nginx/`, `app/`, `static/`)
- [x] 🎨 Interface de démarrage HTML stylée et animée
- [x] 📜 Footer enrichi avec infos personnelles (contact, email, GitHub, portfolio…)
- [x] 🧼 Nettoyage automatique des anciens processus avant démarrage

---

### 🏗️ Fonctionnalités à venir

- [ ] 🧭 Interface graphique Python avec `tkinter` ou `PyQt` pour les non-techs
- [ ] 📊 Page d’accueil avec statistiques PHP (RAM, version, modules actifs, etc.)
- [ ] 🪪 Interface d’authentification pour restreindre l’accès à certaines ressources
- [ ] 🌐 Multi-sites support (accueillir plusieurs projets PHP dans un seul serveur)
- [ ] 🔄 Actualisation automatique du serveur lors des changements de fichiers
- [ ] 🔐 Intégration SSL locale avec `mkcert` (https://localhost)
- [ ] 🧠 Assistant CLI pour ajouter automatiquement un nouveau projet
- [ ] 📁 Configuration dynamique de `nginx.conf` via le script Python

---

### 💡 Fonctionnalités envisagées

> Ce sont des idées ambitieuses, ouvertes à contributions externes :

- 🧬 Plugin système (créer et charger des extensions pour PHPNX)
- 💻 Version Linux portable (avec PHP & NGINX embarqués)
- 📦 Création d’un installeur `.exe` avec **icône Phoenix**
- 🧱 Intégration avec Docker en option
- 🛰️ Mise à jour automatique du launcher via GitHub
- 🧩 Module pour intégrer un éditeur de code minimaliste embarqué

---

### 🧑‍💻 Nous avons besoin de :

| Rôle                | Description                                     |
|---------------------|-------------------------------------------------|
| 💻 Dev Python        | Pour améliorer le launcher et les automatisations |
| 🌐 Dev Web Frontend  | Pour améliorer la page HTML par défaut           |
| ⚙️ Dev Ops           | Pour intégrer Docker et config SSL locale        |
| 🎨 UI/UX Designer    | Pour créer un vrai branding visuel Phoenix       |
| 📖 Rédacteur Docs    | Pour mieux documenter l’usage de chaque module   |

---

## 🤝 Contribuer

Tu es développeur, designer, testeur, devOps, ou juste passionné de belles choses ?
Rejoins le projet. Le Phoenix s’élève avec toi.

Voici comment contribuer :

1. 🍴 Fork ce repo
2. 🚀 Clone ton fork
3. 💻 Crée une branche (git checkout -b feature/mon-idee)
4. 🔥 Cogne du code
5. ✅ Push tes changements (git push origin feature/mon-idee)
6. 📩 Crée une Pull Request

## 🧙‍♂️ Auteur

> Kei Prince Frejuste
> 💼 Web & Software Developer
> 📫 frejuste.dev56@gmail.com
> 🌐 [Portfolio](https://portfolio-edumanagers-projects.vercel.app/) | [GitHub](https://github.com/Frejuste-dev)

---

## 📝 Licence
Ce projet est distribué sous licence MIT.
Fais-en bon usage, mais surtout… fais-le vivre.

> “Comme le Phoenix, tout projet peut renaître de ses cendres. Il suffit d’un peu de code, d’un peu de feu, et d’une grande vision.”

---
