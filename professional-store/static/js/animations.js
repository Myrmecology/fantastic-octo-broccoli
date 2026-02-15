// ========================================
// JUSTIN E-COMMERCE - Animations
// Visual effects and animations
// ========================================

// ============ PARALLAX SCROLL EFFECT ============
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// ============ FLOATING ELEMENTS ============
function animateFloatingElements() {
    const floatingElements = document.querySelectorAll('.floating-icons .cart-icon');
    
    floatingElements.forEach((element, index) => {
        // Random float animation
        const randomDelay = Math.random() * 2;
        const randomDuration = 3 + Math.random() * 3;
        
        element.style.animationDelay = `${randomDelay}s`;
        element.style.animationDuration = `${randomDuration}s`;
    });
}

// ============ MOUSE PARALLAX EFFECT ============
function initMouseParallax() {
    const parallaxContainer = document.querySelector('.landing-hero');
    
    if (!parallaxContainer) return;
    
    document.addEventListener('mousemove', function(e) {
        const icons = document.querySelectorAll('.floating-icons .cart-icon');
        
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        icons.forEach((icon, index) => {
            const speed = (index + 1) * 0.02;
            const x = (mouseX - 0.5) * 100 * speed;
            const y = (mouseY - 0.5) * 100 * speed;
            
            icon.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
}

// ============ FADE IN ON SCROLL ============
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Optional: unobserve after animation
                setTimeout(() => {
                    observer.unobserve(entry.target);
                }, 500);
            }
        });
    }, observerOptions);
    
    // Observe product cards
    document.querySelectorAll('.product-card').forEach(card => {
        observer.observe(card);
    });
    
    // Observe other elements
    document.querySelectorAll('.fade-on-scroll').forEach(element => {
        observer.observe(element);
    });
}

// ============ CARD HOVER GLOW EFFECT ============
function initCardGlowEffect() {
    const cards = document.querySelectorAll('.product-card, .card, .confirmation-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
}

// ============ SMOOTH NUMBER COUNTER ============
function animateCounter(element, target, duration = 1000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = Math.round(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(start);
        }
    }, 16);
}

// ============ PULSE ANIMATION ============
function pulseElement(element, duration = 300) {
    element.style.transition = `transform ${duration}ms ease`;
    element.style.transform = 'scale(1.1)';
    
    setTimeout(() => {
        element.style.transform = 'scale(1)';
    }, duration);
}

// ============ RIPPLE EFFECT ON CLICK ============
function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');
    
    const ripple = button.getElementsByClassName('ripple')[0];
    if (ripple) {
        ripple.remove();
    }
    
    button.appendChild(circle);
    
    setTimeout(() => {
        circle.remove();
    }, 600);
}

// ============ SHAKE ANIMATION (for errors) ============
function shakeElement(element) {
    element.classList.add('shake');
    setTimeout(() => {
        element.classList.remove('shake');
    }, 500);
}

// ============ SLIDE IN ANIMATION ============
function slideIn(element, direction = 'left') {
    element.style.opacity = '0';
    element.style.transform = direction === 'left' ? 'translateX(-50px)' : 'translateX(50px)';
    
    setTimeout(() => {
        element.style.transition = 'all 0.5s ease';
        element.style.opacity = '1';
        element.style.transform = 'translateX(0)';
    }, 10);
}

// ============ TYPING EFFECT ============
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// ============ CONFETTI ANIMATION ============
function createConfetti(count = 50) {
    const colors = ['#4a90e2', '#5dade2', '#c0c5ce', '#8b0000', '#a52a2a'];
    
    for (let i = 0; i < count; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 3 + 's';
            confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
            
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 5000);
        }, i * 30);
    }
}

// ============ LOADING DOTS ANIMATION ============
function animateLoadingDots(element) {
    let dots = 0;
    const maxDots = 3;
    const baseText = element.textContent.replace(/\.+$/, '');
    
    const interval = setInterval(() => {
        dots = (dots + 1) % (maxDots + 1);
        element.textContent = baseText + '.'.repeat(dots);
    }, 500);
    
    // Return function to stop animation
    return () => clearInterval(interval);
}

// ============ PAGE TRANSITION ============
function pageTransition(url) {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease';
    
    setTimeout(() => {
        window.location.href = url;
    }, 300);
}

// ============ INITIALIZATION ============
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations
    initParallax();
    animateFloatingElements();
    initMouseParallax();
    initScrollAnimations();
    initCardGlowEffect();
    
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('button, .btn-primary, .btn-checkout');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });
    
    // Animate counters on page load
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.target);
        animateCounter(counter, target);
    });
    
    console.log('✨ Animations initialized');
});

// ============ CSS ANIMATION CLASSES ============
// Add these to your CSS:
/*
.animate-in {
    animation: fadeInUp 0.6s ease forwards;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.shake {
    animation: shake 0.5s;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
    20%, 40%, 60%, 80% { transform: translateX(10px); }
}

.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    transform: scale(0);
    animation: ripple-animation 0.6s ease-out;
    pointer-events: none;
}

@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.added-to-cart {
    animation: addedToCart 0.6s ease;
}

@keyframes addedToCart {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); box-shadow: 0 0 30px rgba(93, 173, 226, 0.6); }
    100% { transform: scale(1); }
}
*/

// ============ EXPORT FUNCTIONS ============
if (typeof window.JustinEcommerce === 'undefined') {
    window.JustinEcommerce = {};
}

Object.assign(window.JustinEcommerce, {
    animateCounter,
    pulseElement,
    shakeElement,
    slideIn,
    typeWriter,
    createConfetti,
    animateLoadingDots,
    pageTransition
});

// ========================================
// END OF ANIMATIONS
// ========================================