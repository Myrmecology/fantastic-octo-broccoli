# ========================================
# JUSTIN E-COMMERCE - Main Application
# ========================================

from flask import Flask, render_template, session
from flask_session import Session
from config import Config
from models import db, Product, Order, OrderItem, User, Cart
from routes import store_bp, cart_bp, checkout_bp
import os

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
Session(app)

# Register blueprints
app.register_blueprint(store_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)

# Create database tables
def init_db():
    """Initialize database and create tables"""
    with app.app_context():
        # Create database directory if it doesn't exist
        db_dir = os.path.join(os.path.dirname(__file__), 'database')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Create all tables
        db.create_all()
        
        # Load sample data if database is empty
        if Product.query.count() == 0:
            print("Loading sample products...")
            load_sample_products()
        
        print("Database initialized successfully!")

def load_sample_products():
    """Load sample products into database"""
    sample_products = [
        {
            'name': 'Premium Headphones',
            'description': 'High-quality wireless headphones with active noise cancellation. Crystal clear sound and 30-hour battery life.',
            'price': 29999,
            'image_url': '/static/images/products/headphones.jpg',
            'category': 'Electronics',
            'stock': 50,
            'featured': True
        },
        {
            'name': 'Smart Watch',
            'description': 'Advanced fitness tracking and smartphone notifications. Water resistant with heart rate monitoring.',
            'price': 39999,
            'image_url': '/static/images/products/smartwatch.jpg',
            'category': 'Electronics',
            'stock': 30,
            'featured': True
        },
        {
            'name': 'Laptop Stand',
            'description': 'Ergonomic aluminum laptop stand with adjustable height. Improves posture and cooling.',
            'price': 4999,
            'image_url': '/static/images/products/laptop-stand.jpg',
            'category': 'Accessories',
            'stock': 100,
            'featured': False
        },
        {
            'name': 'Mechanical Keyboard',
            'description': 'RGB mechanical gaming keyboard with blue switches. Customizable backlighting and macro keys.',
            'price': 14999,
            'image_url': '/static/images/products/keyboard.jpg',
            'category': 'Electronics',
            'stock': 25,
            'featured': True
        },
        {
            'name': 'Wireless Mouse',
            'description': 'Precision wireless gaming mouse with adjustable DPI. Ergonomic design for long gaming sessions.',
            'price': 7999,
            'image_url': '/static/images/products/mouse.jpg',
            'category': 'Electronics',
            'stock': 75,
            'featured': False
        },
        {
            'name': 'USB-C Hub',
            'description': '7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader, and power delivery. Perfect for laptops.',
            'price': 5999,
            'image_url': '/static/images/products/usb-hub.jpg',
            'category': 'Accessories',
            'stock': 60,
            'featured': False
        },
        {
            'name': 'Phone Case',
            'description': 'Premium leather phone case with card slots. Provides excellent protection and style.',
            'price': 3999,
            'image_url': '/static/images/products/phone-case.jpg',
            'category': 'Accessories',
            'stock': 200,
            'featured': False
        },
        {
            'name': 'Portable Charger',
            'description': '20000mAh fast charging power bank. Charges multiple devices simultaneously.',
            'price': 4999,
            'image_url': '/static/images/products/charger.jpg',
            'category': 'Electronics',
            'stock': 80,
            'featured': False
        }
    ]
    
    for product_data in sample_products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
    print(f"Loaded {len(sample_products)} sample products")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

# Context processor for global variables
@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        'store_name': Config.STORE_NAME,
        'quantum_url': Config.QUANTUM_URL
    }

# Main entry point
if __name__ == '__main__':
    # Initialize database on first run
    if not os.path.exists('database/store.db'):
        print("First run detected - initializing database...")
        init_db()
    
    print("=" * 50)
    print("🚀 JUSTIN E-COMMERCE Server Starting...")
    print("=" * 50)
    print(f"Server running at: http://{Config.HOST}:{Config.PORT}")
    print(f"Quantum project: {Config.QUANTUM_URL}")
    print("=" * 50)
    print("Press CTRL+C to stop the server")
    print("=" * 50)
    
    # Run the app
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=True
    )

# ========================================
# END OF MAIN APPLICATION
# ========================================