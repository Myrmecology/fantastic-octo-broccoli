// ========================================
// JUSTIN E-COMMERCE - Main JavaScript
// ========================================

// ============ INITIALIZATION ============
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 JUSTIN E-COMMERCE - Professional Store Loaded');
    
    // Initialize cart count
    updateCartCount();
    
    // Add smooth scroll behavior
    initSmoothScroll();
    
    // Initialize any animations
    initAnimations();
});

// ============ CART COUNT ============
function updateCartCount() {
    fetch('/api/cart/count')
        .then(response => response.json())
        .then(data => {
            const cartCountElement = document.getElementById('cartCount');
            if (cartCountElement) {
                cartCountElement.textContent = data.count;
                
                // Animate if count changes
                if (data.count > 0) {
                    cartCountElement.classList.add('bounce');
                    setTimeout(() => {
                        cartCountElement.classList.remove('bounce');
                    }, 300);
                }
            }
        })
        .catch(error => console.error('Error updating cart count:', error));
}

// ============ SMOOTH SCROLLING ============
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
}

// ============ ANIMATIONS ============
function initAnimations() {
    // Fade in elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with fade-in class
    document.querySelectorAll('.fade-element').forEach(element => {
        observer.observe(element);
    });
}

// ============ NOTIFICATION SYSTEM ============
function showNotification(message, type = 'success') {
    // Remove any existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Trigger animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// ============ FORM VALIDATION ============
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\(\)\+]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

function validateZip(zip) {
    const re = /^\d{5}(-\d{4})?$/;
    return re.test(zip);
}

// ============ PRICE FORMATTING ============
function formatPrice(cents) {
    return '$' + (cents / 100).toFixed(2);
}

function parsePriceInput(priceString) {
    // Remove $ and convert to cents
    return Math.round(parseFloat(priceString.replace(/[$,]/g, '')) * 100);
}

// ============ LOCAL STORAGE HELPERS ============
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Error saving to localStorage:', error);
        return false;
    }
}

function getFromLocalStorage(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (error) {
        console.error('Error reading from localStorage:', error);
        return null;
    }
}

function removeFromLocalStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (error) {
        console.error('Error removing from localStorage:', error);
        return false;
    }
}

// ============ DEBOUNCE UTILITY ============
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============ LOADING STATE ============
function setLoading(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.dataset.originalText = element.textContent;
        element.innerHTML = '<span class="spinner"></span> Loading...';
    } else {
        element.disabled = false;
        element.textContent = element.dataset.originalText || element.textContent;
    }
}

// ============ ERROR HANDLING ============
function handleError(error, userMessage = 'An error occurred') {
    console.error('Error:', error);
    showNotification(userMessage, 'error');
}

// ============ SCROLL TO TOP ============
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button if page is long
window.addEventListener('scroll', function() {
    const scrollBtn = document.getElementById('scrollToTop');
    if (scrollBtn) {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    }
});

// ============ EXPORT FUNCTIONS ============
// Make functions available globally
window.JustinEcommerce = {
    updateCartCount,
    showNotification,
    formatPrice,
    validateEmail,
    validatePhone,
    validateZip,
    setLoading,
    handleError,
    scrollToTop,
    debounce
};

// ========================================
// END OF MAIN JAVASCRIPT
// ========================================