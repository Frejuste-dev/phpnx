<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHPNX - Le Phoenix s'élève !</title>
    <link rel="stylesheet" href="/style.css">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="phoenix-icon">🔥</div>
            <h1>PHPNX</h1>
            <p class="subtitle">Le Phoenix s'élève !</p>
        </header>

        <main class="main-content">
            <div class="welcome-section">
                <h2>🎉 Bienvenue sur votre serveur PHPNX</h2>
                <p>Votre environnement de développement PHP est prêt et fonctionne parfaitement !</p>
            </div>

            <div class="info-grid">
                <div class="info-card">
                    <h3>🐍 PHP</h3>
                    <p><strong>Version :</strong> <?php echo phpversion(); ?></p>
                    <p><strong>Serveur :</strong> <?php echo $_SERVER['SERVER_SOFTWARE'] ?? 'FastCGI'; ?></p>
                    <a href="/phpinfo" class="btn">Voir phpinfo()</a>
                </div>

                <div class="info-card">
                    <h3>🌐 Serveur</h3>
                    <p><strong>Host :</strong> <?php echo $_SERVER['HTTP_HOST']; ?></p>
                    <p><strong>Port :</strong> <?php echo $_SERVER['SERVER_PORT']; ?></p>
                    <p><strong>Protocole :</strong> <?php echo $_SERVER['SERVER_PROTOCOL']; ?></p>
                </div>

                <div class="info-card">
                    <h3>📊 Système</h3>
                    <p><strong>OS :</strong> <?php echo PHP_OS; ?></p>
                    <p><strong>Architecture :</strong> <?php echo php_uname('m'); ?></p>
                    <p><strong>Mémoire :</strong> <?php echo ini_get('memory_limit'); ?></p>
                </div>

                <div class="info-card">
                    <h3>🕐 Temps</h3>
                    <p><strong>Heure serveur :</strong> <?php echo date('H:i:s'); ?></p>
                    <p><strong>Date :</strong> <?php echo date('d/m/Y'); ?></p>
                    <p><strong>Timezone :</strong> <?php echo date_default_timezone_get(); ?></p>
                </div>
            </div>

            <div class="extensions-section">
                <h3>🧩 Extensions PHP Chargées</h3>
                <div class="extensions-grid">
                    <?php
                    $extensions = get_loaded_extensions();
                    sort($extensions);
                    foreach (array_slice($extensions, 0, 12) as $extension) {
                        echo "<span class='extension-badge'>{$extension}</span>";
                    }
                    if (count($extensions) > 12) {
                        echo "<span class='extension-badge more'>+" . (count($extensions) - 12) . " autres</span>";
                    }
                    ?>
                </div>
            </div>

            <div class="quick-actions">
                <h3>🚀 Actions Rapides</h3>
                <div class="actions-grid">
                    <a href="/phpinfo" class="action-btn">
                        <span class="icon">📋</span>
                        <span>PHP Info</span>
                    </a>
                    <a href="/" class="action-btn">
                        <span class="icon">🏠</span>
                        <span>Accueil</span>
                    </a>
                    <a href="#" onclick="window.location.reload()" class="action-btn">
                        <span class="icon">🔄</span>
                        <span>Actualiser</span>
                    </a>
                </div>
            </div>
        </main>

        <footer class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>🔥 PHPNX</h4>
                    <p>Environnement de développement PHP portable et élégant</p>
                </div>
                <div class="footer-section">
                    <h4>👨‍💻 Développeur</h4>
                    <p><strong>Kei Prince Frejuste</strong></p>
                    <p>Web & Software Developer</p>
                </div>
                <div class="footer-section">
                    <h4>📞 Contact</h4>
                    <p>📧 <a href="mailto:keifrejuste26@gmail.com">keifrejuste26@gmail.com</a></p>
                    <p>🌐 <a href="https://portfolio-edumanagers-projects.vercel.app/" target="_blank">Portfolio</a></p>
                    <p>💻 <a href="https://github.com/frejuste26" target="_blank">GitHub</a></p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <?php echo date('Y'); ?> PHPNX - Le Phoenix s'élève ! Comme le Phoenix, tout projet peut renaître de ses cendres.</p>
            </div>
        </footer>
    </div>

    <script src="/script.js"></script>
</body>
</html>
