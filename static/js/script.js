// PHPNX - Le Phoenix s'élève !
// Scripts pour l'interactivité et les effets visuels

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des effets Phoenix
    initPhoenixEffects();
    
    // Gestion des animations d'entrée
    initScrollAnimations();
    
    // Horloge en temps réel
    initRealtimeClock();
    
    // Effets de particules
    initParticleEffects();
    
    console.log('🔥 PHPNX - Le Phoenix s\'élève !');
});

// Effets Phoenix principaux
function initPhoenixEffects() {
    const phoenixIcon = document.querySelector('.phoenix-icon');
    
    if (phoenixIcon) {
        // Effet de clic sur l'icône Phoenix
        phoenixIcon.addEventListener('click', function() {
            this.style.animation = 'none';
            this.style.transform = 'scale(1.5) rotate(360deg)';
            this.style.transition = 'all 0.6s ease';
            
            setTimeout(() => {
                this.style.animation = 'phoenixFlame 2s ease-in-out infinite alternate';
                this.style.transform = '';
                this.style.transition = '';
            }, 600);
        });
        
        // Effet de survol
        phoenixIcon.addEventListener('mouseenter', function() {
            this.style.filter = 'brightness(1.3) saturate(1.2)';
        });
        
        phoenixIcon.addEventListener('mouseleave', function() {
            this.style.filter = '';
        });
    }
}

// Animations au scroll
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observer les cartes d'information
    document.querySelectorAll('.info-card').forEach(card => {
        observer.observe(card);
    });
    
    // Observer les sections
    document.querySelectorAll('.extensions-section, .quick-actions').forEach(section => {
        observer.observe(section);
    });
}

// Horloge en temps réel
function initRealtimeClock() {
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('fr-FR');
        const dateString = now.toLocaleDateString('fr-FR');
        
        // Mettre à jour l'heure si l'élément existe
        const timeElements = document.querySelectorAll('.info-card p');
        timeElements.forEach(element => {
            if (element.innerHTML.includes('Heure serveur')) {
                element.innerHTML = `<strong>Heure serveur :</strong> ${timeString}`;
            }
            if (element.innerHTML.includes('Date')) {
                element.innerHTML = `<strong>Date :</strong> ${dateString}`;
            }
        });
    }
    
    // Mettre à jour toutes les secondes
    setInterval(updateClock, 1000);
}

// Effets de particules Phoenix
function initParticleEffects() {
    const header = document.querySelector('.header');
    
    if (header) {
        createFloatingEmbers(header);
    }
}

function createFloatingEmbers(container) {
    const emberCount = 15;
    const embers = [];
    
    for (let i = 0; i < emberCount; i++) {
        const ember = document.createElement('div');
        ember.className = 'floating-ember';
        ember.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: linear-gradient(45deg, #dc2626, #ea580c);
            border-radius: 50%;
            pointer-events: none;
            opacity: 0;
            z-index: 1;
        `;
        
        container.appendChild(ember);
        embers.push(ember);
        
        animateEmber(ember, container);
    }
}

function animateEmber(ember, container) {
    const containerRect = container.getBoundingClientRect();
    const startX = Math.random() * containerRect.width;
    const startY = containerRect.height;
    
    ember.style.left = startX + 'px';
    ember.style.top = startY + 'px';
    ember.style.opacity = '0.8';
    
    const animation = ember.animate([
        {
            transform: 'translate(0, 0) scale(1)',
            opacity: 0.8
        },
        {
            transform: `translate(${(Math.random() - 0.5) * 100}px, -${containerRect.height + 50}px) scale(0.5)`,
            opacity: 0
        }
    ], {
        duration: 3000 + Math.random() * 2000,
        easing: 'ease-out'
    });
    
    animation.onfinish = () => {
        setTimeout(() => {
            animateEmber(ember, container);
        }, Math.random() * 2000);
    };
}

// Effets sur les cartes d'information
document.querySelectorAll('.info-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.background = 'linear-gradient(135deg, #1f2937 0%, #374151 100%)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.background = '#1f2937';
    });
});

// Effet de typing pour le titre
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Gestion des erreurs de chargement des images
document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function() {
        this.style.display = 'none';
    });
});

// Notification de bienvenue
function showWelcomeNotification() {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(45deg, #dc2626, #ea580c);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(220, 38, 38, 0.3);
        z-index: 1000;
        font-weight: bold;
        transform: translateX(300px);
        transition: transform 0.3s ease;
    `;
    
    notification.innerHTML = '🔥 PHPNX est prêt !';
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 500);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(300px)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Lancer la notification après le chargement
setTimeout(showWelcomeNotification, 1000);

// Gestion du thème (pour futures versions)
function toggleTheme() {
    document.body.classList.toggle('light-theme');
    localStorage.setItem('theme', document.body.classList.contains('light-theme') ? 'light' : 'dark');
}

// Statistiques de performance simples
function logPerformanceStats() {
    if (performance.timing) {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`🚀 Page chargée en ${loadTime}ms`);
    }
}

window.addEventListener('load', logPerformanceStats);

// Gestion des touches de raccourci
document.addEventListener('keydown', function(e) {
    // Ctrl + R pour rafraîchir
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        location.reload();
    }
    
    // Ctrl + I pour PHP Info
    if (e.ctrlKey && e.key === 'i') {
        e.preventDefault();
        window.location.href = '/phpinfo';
    }
});

// Détection de la connexion réseau
window.addEventListener('online', function() {
    console.log('🌐 Connexion réseau rétablie');
});

window.addEventListener('offline', function() {
    console.log('📴 Connexion réseau perdue');
});

// Smooth scroll pour les liens internes
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Ajout d'une classe CSS pour les animations
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
        transition: all 0.6s ease !important;
    }
    
    .info-card {
        opacity: 0;
        transform: translateY(30px);
    }
    
    .floating-ember {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
`;
document.head.appendChild(style);