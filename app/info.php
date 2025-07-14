<?php
/**
 * PHPNX - Le Phoenix s'élève !
 * Page d'informations PHP avec style personnalisé
 */

// Configuration pour une sortie propre
ob_start();
phpinfo();
$phpinfo = ob_get_clean();

// Personnalisation du style phpinfo
$phpinfo = preg_replace(
    '/<style type="text\/css">(.*?)<\/style>/s',
    '<style type="text/css">
    body { 
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        color: #f9fafb;
        margin: 0;
        padding: 20px;
    }
    
    .center { 
        text-align: center;
        margin: 20px 0;
    }
    
    .center table { 
        margin: 0 auto;
        background: #1f2937;
        border-radius: 10px;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    table { 
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        background: #1f2937;
        border-radius: 10px;
        overflow: hidden;
    }
    
    th, td { 
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #374151;
    }
    
    th { 
        background: linear-gradient(45deg, #dc2626, #ea580c);
        color: white;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    tr:nth-child(even) { 
        background: #374151;
    }
    
    tr:hover { 
        background: #4b5563;
        transition: background 0.3s ease;
    }
    
    .p { 
        color: #f9fafb;
        margin: 10px 0;
    }
    
    .e { 
        background: #dc2626 !important;
        color: white !important;
        font-weight: bold;
        padding: 8px 12px;
        border-radius: 5px;
    }
    
    .v { 
        background: #1f2937 !important;
        color: #9ca3af;
        font-family: "Courier New", monospace;
        font-size: 0.9em;
    }
    
    .h { 
        background: linear-gradient(45deg, #dc2626, #ea580c) !important;
        color: white !important;
        font-size: 1.2em;
        font-weight: bold;
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    hr { 
        border: none;
        height: 2px;
        background: linear-gradient(45deg, #dc2626, #ea580c);
        margin: 30px 0;
        border-radius: 1px;
    }
    
    img { 
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    a { 
        color: #3b82f6;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    a:hover { 
        color: #ea580c;
    }
    
    .header-phoenix {
        text-align: center;
        padding: 40px 0;
        background: rgba(31, 41, 55, 0.6);
        border-radius: 15px;
        margin-bottom: 30px;
        border: 1px solid #374151;
    }
    
    .phoenix-title {
        font-size: 2.5em;
        background: linear-gradient(45deg, #dc2626, #ea580c, #d97706, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .phoenix-subtitle {
        color: #9ca3af;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
    
    .back-button {
        display: inline-block;
        padding: 10px 20px;
        background: linear-gradient(45deg, #dc2626, #ea580c);
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
        margin: 20px 0;
    }
    
    .back-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(220, 38, 38, 0.4);
        color: white;
    }
    
    @media (max-width: 768px) {
        body { padding: 10px; }
        table { font-size: 0.8em; }
        th, td { padding: 8px 10px; }
    }
    </style>',
    $phpinfo
);

// Ajouter un header personnalisé
$header = '<div class="header-phoenix">
    <div class="phoenix-title">🔥 PHPNX - PHP Info</div>
    <div class="phoenix-subtitle">Le Phoenix s\'élève avec PHP !</div>
    <a href="/" class="back-button">← Retour à l\'accueil</a>
</div>';

$phpinfo = str_replace('<body>', '<body>' . $header, $phpinfo);

// Ajouter des informations supplémentaires spécifiques à PHPNX
$phpnx_info = '<div class="header-phoenix">
    <h2>🔥 Informations PHPNX</h2>
    <table>
        <tr><th>Paramètre</th><th>Valeur</th></tr>
        <tr><td>Version PHPNX</td><td>1.0.0</td></tr>
        <tr><td>Serveur Web</td><td>NGINX + PHP FastCGI</td></tr>
        <tr><td>Mode</td><td>Développement Portable</td></tr>
        <tr><td>Environnement</td><td>Local</td></tr>
        <tr><td>Auteur</td><td>Kei Prince Frejuste</td></tr>
        <tr><td>Contact</td><td>keifrejuste26@gmail.com</td></tr>
    </table>
</div>';

$phpinfo = str_replace('</body>', $phpnx_info . '</body>', $phpinfo);

// Afficher le résultat
echo $phpinfo;
?>
