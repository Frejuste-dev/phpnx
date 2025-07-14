<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>🔥 PHPNX - Le Phoenix s'élève</title>
    <link rel="icon" href="/static/favicon.ico">
    <style>
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            font-family: 'Segoe UI', sans-serif;
            padding: 2rem;
        }
        header h1 { font-size: 2.5rem; color: #ff6f61; animation: rise 2s ease; text-align: center; }
        main pre { background: #111; padding: 1rem; border-radius: 8px; color: #00ffcc; overflow: auto; }
        footer {
            margin-top: 2rem;
            background: #111;
            padding: 2rem;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            color: #ccc;
        }
        footer a { color: #0ff; text-decoration: none; }
        footer a:hover { text-decoration: underline; }
        .footer-section { min-width: 200px; margin: 1rem; }
        .footer-section h3 { color: #ffcc00; margin-bottom: 0.5rem; }

        @keyframes rise {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
    </style>
</head>
<body>
<header>
    <h1>🔥 Bienvenue sur PHPNX - Le Phoenix s'élève !</h1>
</header>
<main>
    <h2>📜 Informations PHP</h2>
    <pre><?php phpinfo(); ?></pre>
</main>
<footer>
    <div class="footer-section">
        <h3>📞 Contact</h3>
        <p>Tél : <a href="tel:+2250700000000">+225 07 00 00 00 00</a></p>
        <p>Email : <a href="mailto:frejuste.dev@gmail.com">frejuste.dev@gmail.com</a></p>
    </div>
    <div class="footer-section">
        <h3>🧠 Développement</h3>
        <p>Kei Prince Frejuste</p>
        <p>Web & Software Engineer</p>
    </div>
    <div class="footer-section">
        <h3>🌍 Liens</h3>
        <p><a href="https://github.com/frejuste" target="_blank">GitHub</a></p>
        <p><a href="https://frejuste.dev" target="_blank">Portfolio</a></p>
        <p><a href="/cv.pdf" target="_blank">Mon CV</a></p>
    </div>
</footer>
</body>
</html>
