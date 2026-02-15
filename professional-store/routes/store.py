# ========================================
# JUSTIN E-COMMERCE - Store Routes
# ========================================

from flask import Blueprint, render_template, request, jsonify
from models import db, Product
from sqlalchemy import or_

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def landing():
    """Landing page - JUSTIN E-COMMERCE splash screen"""
    return render_template('landing.html')

@store_bp.route('/store')
def store():
    """Main store page - product catalog"""
    # Get query parameters
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    sort = request.args.get('sort', 'featured')
    
    # Base query - only active products
    query = Product.query.filter_by(active=True)
    
    # Filter by category
    if category:
        query = query.filter_by(category=category)
    
    # Search functionality
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
    
    # Sorting
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'name':
        query = query.order_by(Product.name.asc())
    else:  # featured (default)
        query = query.order_by(Product.featured.desc(), Product.created_at.desc())
    
    products = query.all()
    
    # Get all categories for filter
    categories = db.session.query(Product.category).filter_by(active=True).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template(
        'store.html',
        products=products,
        categories=categories,
        selected_category=category,
        search_query=search,
        sort_by=sort
    )

@store_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    
    # Get related products (same category, excluding current)
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id,
        Product.active == True
    ).limit(4).all()
    
    return render_template(
        'product.html',
        product=product,
        related_products=related_products
    )

@store_bp.route('/api/products')
def api_products():
    """API endpoint for products (AJAX/JSON)"""
    products = Product.query.filter_by(active=True).all()
    return jsonify([product.to_dict() for product in products])

@store_bp.route('/api/product/<int:product_id>')
def api_product(product_id):
    """API endpoint for single product"""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@store_bp.route('/search')
def search():
    """Search endpoint"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify([])
    
    search_term = f"%{query}%"
    products = Product.query.filter(
        Product.active == True,
        or_(
            Product.name.ilike(search_term),
            Product.description.ilike(search_term),
            Product.category.ilike(search_term)
        )
    ).limit(10).all()
    
    return jsonify([product.to_dict() for product in products])

# ========================================
# END OF STORE ROUTES
# ========================================