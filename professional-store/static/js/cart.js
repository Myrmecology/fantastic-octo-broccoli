// ========================================
// JUSTIN E-COMMERCE - Cart JavaScript
// Shopping cart functionality
// ========================================

// ============ ADD TO CART ============
function addToCart(productId, quantity = 1) {
    // Disable add button temporarily
    const addButtons = document.querySelectorAll(`[onclick*="addToCart(${productId})"]`);
    addButtons.forEach(btn => btn.disabled = true);
    
    fetch('/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart count in navbar
            updateCartCount(data.cart_count);
            
            // Show success notification
            showNotification('✅ Product added to cart!', 'success');
            
            // Re-enable buttons
            addButtons.forEach(btn => btn.disabled = false);
        } else {
            showNotification('❌ Error: ' + data.error, 'error');
            addButtons.forEach(btn => btn.disabled = false);
        }
    })
    .catch(error => {
        console.error('Error adding to cart:', error);
        showNotification('❌ Error adding to cart', 'error');
        addButtons.forEach(btn => btn.disabled = false);
    });
}

// ============ UPDATE CART QUANTITY ============
function updateCartQuantity(cartItemId, newQuantity) {
    if (newQuantity < 1) {
        removeFromCart(cartItemId);
        return;
    }
    
    fetch('/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cart_item_id: cartItemId,
            quantity: newQuantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload page to update totals
            location.reload();
        } else {
            showNotification('❌ Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error updating cart:', error);
        showNotification('❌ Error updating cart', 'error');
    });
}

// ============ REMOVE FROM CART ============
function removeFromCart(cartItemId) {
    if (!confirm('Remove this item from your cart?')) {
        return;
    }
    
    fetch(`/cart/remove/${cartItemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove item from DOM
            const itemElement = document.getElementById(`cart-item-${cartItemId}`);
            if (itemElement) {
                itemElement.style.opacity = '0';
                itemElement.style.transform = 'translateX(-100%)';
                
                setTimeout(() => {
                    itemElement.remove();
                    
                    // Check if cart is now empty
                    const remainingItems = document.querySelectorAll('.cart-item');
                    if (remainingItems.length === 0) {
                        location.reload();
                    } else {
                        location.reload(); // Reload to update totals
                    }
                }, 300);
            }
            
            showNotification('✅ Item removed from cart', 'success');
        } else {
            showNotification('❌ Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error removing item:', error);
        showNotification('❌ Error removing item', 'error');
    });
}

// ============ CLEAR CART ============
function clearCart() {
    if (!confirm('Clear all items from your cart?')) {
        return;
    }
    
    fetch('/cart/clear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('✅ Cart cleared', 'success');
            setTimeout(() => {
                location.reload();
            }, 500);
        } else {
            showNotification('❌ Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error clearing cart:', error);
        showNotification('❌ Error clearing cart', 'error');
    });
}

// ============ UPDATE CART COUNT ============
function updateCartCount(count) {
    const cartCountElement = document.getElementById('cartCount');
    if (cartCountElement) {
        cartCountElement.textContent = count || 0;
        
        // Animate count change
        cartCountElement.style.transform = 'scale(1.3)';
        setTimeout(() => {
            cartCountElement.style.transform = 'scale(1)';
        }, 200);
    }
}

// ============ GET CART TOTAL ============
function getCartTotal() {
    return fetch('/api/cart/items')
        .then(response => response.json())
        .then(items => {
            let total = 0;
            items.forEach(item => {
                total += item.subtotal;
            });
            return total;
        })
        .catch(error => {
            console.error('Error getting cart total:', error);
            return 0;
        });
}

// ============ VALIDATE CART BEFORE CHECKOUT ============
function validateCartBeforeCheckout() {
    return fetch('/api/cart/items')
        .then(response => response.json())
        .then(items => {
            if (items.length === 0) {
                showNotification('❌ Your cart is empty', 'error');
                return false;
            }
            
            // Check stock availability
            for (let item of items) {
                if (item.product && !item.product.in_stock) {
                    showNotification(`❌ ${item.product.name} is out of stock`, 'error');
                    return false;
                }
                
                if (item.product && item.quantity > item.product.stock) {
                    showNotification(`❌ Only ${item.product.stock} ${item.product.name} available`, 'error');
                    return false;
                }
            }
            
            return true;
        })
        .catch(error => {
            console.error('Error validating cart:', error);
            showNotification('❌ Error validating cart', 'error');
            return false;
        });
}

// ============ MINI CART PREVIEW (Optional) ============
function showMiniCart() {
    fetch('/api/cart/items')
        .then(response => response.json())
        .then(items => {
            if (items.length === 0) {
                showNotification('Your cart is empty', 'info');
                return;
            }
            
            // Create mini cart preview
            let cartHTML = '<div class="mini-cart">';
            cartHTML += '<h3>Your Cart</h3>';
            
            items.forEach(item => {
                cartHTML += `
                    <div class="mini-cart-item">
                        <span>${item.product.name} x ${item.quantity}</span>
                        <span>${item.subtotal_formatted}</span>
                    </div>
                `;
            });
            
            cartHTML += '</div>';
            
            // Could display this in a modal or tooltip
            console.log('Mini cart:', items);
        })
        .catch(error => {
            console.error('Error loading mini cart:', error);
        });
}

// ============ CART PAGE INITIALIZATION ============
document.addEventListener('DOMContentLoaded', function() {
    // Add quantity change listeners if on cart page
    const quantityInputs = document.querySelectorAll('.cart-item input[type="number"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const cartItemId = this.closest('.cart-item').id.replace('cart-item-', '');
            const newQuantity = parseInt(this.value);
            updateCartQuantity(cartItemId, newQuantity);
        });
    });
    
    // Prevent manual input in quantity fields (use buttons only)
    quantityInputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            e.preventDefault();
        });
    });
});

// ============ QUICK ADD TO CART ANIMATION ============
function quickAddAnimation(productId) {
    const productCard = document.querySelector(`[data-product-id="${productId}"]`);
    if (productCard) {
        productCard.classList.add('added-to-cart');
        setTimeout(() => {
            productCard.classList.remove('added-to-cart');
        }, 600);
    }
}

// ============ EXPORT FUNCTIONS ============
if (typeof window.JustinEcommerce === 'undefined') {
    window.JustinEcommerce = {};
}

Object.assign(window.JustinEcommerce, {
    addToCart,
    updateCartQuantity,
    removeFromCart,
    clearCart,
    updateCartCount,
    getCartTotal,
    validateCartBeforeCheckout
});

// ========================================
// END OF CART JAVASCRIPT
// ========================================