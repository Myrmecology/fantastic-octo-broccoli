# ========================================
# JUSTIN E-COMMERCE - Cart Routes
# ========================================

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import db, Product, Cart
import uuid

cart_bp = Blueprint('cart', __name__)

def get_session_id():
    """Get or create session ID for cart"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@cart_bp.route('/cart')
def view_cart():
    """View shopping cart"""
    session_id = get_session_id()
    
    # Get cart items for this session
    cart_items = Cart.query.filter_by(session_id=session_id).all()
    
    # Calculate totals
    subtotal = sum(item.get_subtotal() for item in cart_items)
    tax_rate = 0.0825  # 8.25%
    tax = int(subtotal * tax_rate)
    shipping = 999  # $9.99
    total = subtotal + tax + shipping
    
    return render_template(
        'cart.html',
        cart_items=cart_items,
        subtotal=subtotal,
        tax=tax,
        shipping=shipping,
        total=total
    )

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400
    
    # Verify product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Check stock
    if product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    session_id = get_session_id()
    
    # Check if item already in cart
    cart_item = Cart.query.filter_by(
        session_id=session_id,
        product_id=product_id
    ).first()
    
    if cart_item:
        # Update quantity
        cart_item.quantity += quantity
    else:
        # Create new cart item
        cart_item = Cart(
            session_id=session_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    # Get cart count
    cart_count = Cart.query.filter_by(session_id=session_id).count()
    
    return jsonify({
        'success': True,
        'message': 'Product added to cart',
        'cart_count': cart_count,
        'cart_item': cart_item.to_dict()
    })

@cart_bp.route('/cart/update', methods=['POST'])
def update_cart():
    """Update cart item quantity"""
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    quantity = data.get('quantity', 1)
    
    if not cart_item_id:
        return jsonify({'error': 'Cart item ID required'}), 400
    
    session_id = get_session_id()
    
    cart_item = Cart.query.filter_by(
        id=cart_item_id,
        session_id=session_id
    ).first()
    
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    # Check stock
    if cart_item.product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cart updated',
        'cart_item': cart_item.to_dict() if quantity > 0 else None
    })

@cart_bp.route('/cart/remove/<int:cart_item_id>', methods=['POST', 'DELETE'])
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    session_id = get_session_id()
    
    cart_item = Cart.query.filter_by(
        id=cart_item_id,
        session_id=session_id
    ).first()
    
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Item removed from cart'
    })

@cart_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    """Clear all items from cart"""
    session_id = get_session_id()
    
    Cart.query.filter_by(session_id=session_id).delete()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cart cleared'
    })

@cart_bp.route('/api/cart/count')
def cart_count():
    """Get cart item count"""
    session_id = get_session_id()
    count = Cart.query.filter_by(session_id=session_id).count()
    
    return jsonify({'count': count})

@cart_bp.route('/api/cart/items')
def cart_items_api():
    """Get cart items as JSON"""
    session_id = get_session_id()
    cart_items = Cart.query.filter_by(session_id=session_id).all()
    
    return jsonify([item.to_dict() for item in cart_items])

# ========================================
# END OF CART ROUTES
# ========================================