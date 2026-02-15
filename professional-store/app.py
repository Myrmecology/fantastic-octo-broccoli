# ========================================
# JUSTIN E-COMMERCE - Main Application
# ========================================

from flask import Flask, render_template
from flask_session import Session
from config import Config
import os

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
Session(app)

# Import and initialize database AFTER app is created
from models import db
db.init_app(app)

# Import models AFTER db is initialized
from models import Product, Order, OrderItem, User, Cart

# Import and register blueprints
from routes import store_bp, cart_bp, checkout_bp
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
    """Load 60 sample products into database - Amazon-style catalog"""
    sample_products = [
        # ELECTRONICS - Premium Items
        {
            'name': 'Premium Wireless Headphones',
            'description': 'Active noise cancellation, 30-hour battery, premium sound quality. Perfect for music lovers.',
            'price': 29999,
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 50,
            'featured': True
        },
        {
            'name': 'Smart Watch Pro',
            'description': 'Fitness tracking, heart rate monitor, GPS, water resistant. Stay connected and healthy.',
            'price': 39999,
            'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 30,
            'featured': True
        },
        {
            'name': 'Mechanical Gaming Keyboard',
            'description': 'RGB backlit, blue switches, anti-ghosting, programmable macros. Ultimate gaming experience.',
            'price': 14999,
            'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 25,
            'featured': True
        },
        {
            'name': 'Wireless Gaming Mouse',
            'description': 'Precision optical sensor, adjustable DPI, ergonomic design, RGB lighting.',
            'price': 7999,
            'image_url': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 75,
            'featured': False
        },
        {
            'name': '4K Webcam',
            'description': 'Ultra HD video, auto-focus, built-in microphone. Perfect for streaming and video calls.',
            'price': 12999,
            'image_url': 'https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 40,
            'featured': False
        },
        {
            'name': 'USB-C Hub 7-in-1',
            'description': 'HDMI, USB 3.0, SD card reader, power delivery. Essential laptop accessory.',
            'price': 5999,
            'image_url': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 60,
            'featured': False
        },
        {
            'name': 'Portable SSD 1TB',
            'description': 'Ultra-fast storage, compact design, USB-C compatible. Store everything securely.',
            'price': 11999,
            'image_url': 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 35,
            'featured': False
        },
        {
            'name': 'Bluetooth Speaker',
            'description': 'Waterproof, 20-hour battery, 360-degree sound. Perfect for outdoor adventures.',
            'price': 8999,
            'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 55,
            'featured': False
        },
        {
            'name': 'Laptop Stand Aluminum',
            'description': 'Ergonomic design, adjustable height, improved cooling. Better posture guaranteed.',
            'price': 4999,
            'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 100,
            'featured': False
        },
        {
            'name': 'Wireless Earbuds',
            'description': 'True wireless, charging case, touch controls, crystal clear sound.',
            'price': 9999,
            'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 80,
            'featured': True
        },
        
        # CLOTHING & FASHION
        {
            'name': 'Classic Denim Jacket',
            'description': 'Timeless style, premium denim, comfortable fit. A wardrobe essential.',
            'price': 7999,
            'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop',
            'category': 'Clothing',
            'stock': 45,
            'featured': True
        },
        {
            'name': 'Cotton T-Shirt Pack (3)',
            'description': 'Soft cotton, various colors, comfortable fit. Everyday basics.',
            'price': 2999,
            'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
            'category': 'Clothing',
            'stock': 150,
            'featured': False
        },
        {
            'name': 'Running Shoes',
            'description': 'Lightweight, breathable, cushioned sole. Perfect for your daily run.',
            'price': 8999,
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
            'category': 'Clothing',
            'stock': 65,
            'featured': True
        },
        {
            'name': 'Leather Wallet',
            'description': 'Genuine leather, multiple card slots, slim design. Classic and practical.',
            'price': 3999,
            'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=400&fit=crop',
            'category': 'Accessories',
            'stock': 90,
            'featured': False
        },
        {
            'name': 'Backpack Laptop',
            'description': 'Padded laptop compartment, water resistant, multiple pockets. Urban essential.',
            'price': 6999,
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop',
            'category': 'Accessories',
            'stock': 70,
            'featured': False
        },
        {
            'name': 'Sunglasses Polarized',
            'description': 'UV protection, polarized lenses, stylish frames. Protect your eyes in style.',
            'price': 4999,
            'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400&h=400&fit=crop',
            'category': 'Accessories',
            'stock': 85,
            'featured': False
        },
        {
            'name': 'Baseball Cap',
            'description': 'Adjustable fit, breathable fabric, classic design. Casual everyday wear.',
            'price': 1999,
            'image_url': 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop',
            'category': 'Accessories',
            'stock': 120,
            'featured': False
        },
        {
            'name': 'Hooded Sweatshirt',
            'description': 'Soft fleece, kangaroo pocket, relaxed fit. Cozy comfort for any season.',
            'price': 4999,
            'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop',
            'category': 'Clothing',
            'stock': 95,
            'featured': False
        },
        
        # HOME & GARDEN
        {
            'name': 'Coffee Maker Automatic',
            'description': 'Programmable, 12-cup capacity, auto shut-off. Wake up to fresh coffee.',
            'price': 7999,
            'image_url': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 40,
            'featured': True
        },
        {
            'name': 'Blender High-Speed',
            'description': 'Powerful motor, multiple speeds, easy to clean. Perfect for smoothies.',
            'price': 9999,
            'image_url': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 35,
            'featured': False
        },
        {
            'name': 'Air Fryer 5Qt',
            'description': 'Healthier cooking, digital controls, dishwasher safe. Crispy without the oil.',
            'price': 12999,
            'image_url': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 28,
            'featured': True
        },
        {
            'name': 'Vacuum Cleaner Robot',
            'description': 'Smart navigation, auto-charging, app control. Clean floors effortlessly.',
            'price': 29999,
            'image_url': 'https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 22,
            'featured': True
        },
        {
            'name': 'LED Desk Lamp',
            'description': 'Adjustable brightness, USB charging port, eye-care technology.',
            'price': 3999,
            'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 75,
            'featured': False
        },
        {
            'name': 'Throw Pillow Set (4)',
            'description': 'Soft fabric, decorative patterns, machine washable. Refresh your living space.',
            'price': 3499,
            'image_url': 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 60,
            'featured': False
        },
        {
            'name': 'Indoor Plant Potted',
            'description': 'Low maintenance, air purifying, ceramic pot included. Bring nature indoors.',
            'price': 2999,
            'image_url': 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 50,
            'featured': False
        },
        {
            'name': 'Bath Towel Set',
            'description': 'Ultra-soft, absorbent, fade-resistant. Hotel quality for your home.',
            'price': 4999,
            'image_url': 'https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 80,
            'featured': False
        },
        
        # SPORTS & OUTDOORS
        {
            'name': 'Yoga Mat Premium',
            'description': 'Non-slip, extra thick, eco-friendly. Perfect for yoga and workouts.',
            'price': 3999,
            'image_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop',
            'category': 'Sports',
            'stock': 70,
            'featured': True
        },
        {
            'name': 'Dumbbell Set Adjustable',
            'description': 'Easy weight adjustment, compact design, non-slip grip. Home gym essential.',
            'price': 14999,
            'image_url': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=400&fit=crop',
            'category': 'Sports',
            'stock': 35,
            'featured': True
        },
        {
            'name': 'Water Bottle Insulated',
            'description': 'Keeps cold 24hrs, stainless steel, leak-proof. Stay hydrated all day.',
            'price': 2999,
            'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop',
            'category': 'Sports',
            'stock': 150,
            'featured': False
        },
        {
            'name': 'Resistance Bands Set',
            'description': 'Multiple resistance levels, portable, includes carry bag. Workout anywhere.',
            'price': 1999,
            'image_url': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400&h=400&fit=crop',
            'category': 'Sports',
            'stock': 90,
            'featured': False
        },
        {
            'name': 'Camping Tent 4-Person',
            'description': 'Waterproof, easy setup, ventilation windows. Perfect for family camping.',
            'price': 12999,
            'image_url': 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400&h=400&fit=crop',
            'category': 'Sports',
            'stock': 25,
            'featured': False
        },
        {
            'name': 'Sleeping Bag',
            'description': 'Warm, lightweight, compact storage. Comfortable outdoor sleeping.',
            'price': 5999,
            'image_url': 'https://images.unsplash.com/photo-1520095972714-909e91b038e5?w=400&h=400&fit=crop',
            'category': 'Sports',
            'stock': 45,
            'featured': False
        },
        {
            'name': 'Hiking Backpack 40L',
            'description': 'Multiple compartments, hydration compatible, adjustable straps.',
            'price': 8999,
            'image_url': 'https://images.unsplash.com/photo-1622260614153-03223fb72052?w=400&h=400&fit=crop',
            'category': 'Sports',
            'stock': 40,
            'featured': False
        },
        {
            'name': 'Bike Helmet',
            'description': 'Safety certified, adjustable fit, ventilation. Ride safely.',
            'price': 4999,
            'image_url': 'https://images.unsplash.com/photo-1567586679949-ba5e4a1c3f35?w=400&h=400&fit=crop',
            'category': 'Sports',
            'stock': 60,
            'featured': False
        },
        
        # BOOKS & MEDIA
        {
            'name': 'Bestseller Fiction Book',
            'description': 'Page-turner mystery novel, award-winning author. Perfect for book lovers.',
            'price': 1499,
            'image_url': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop',
            'category': 'Books',
            'stock': 200,
            'featured': False
        },
        {
            'name': 'Cookbook Healthy Recipes',
            'description': '300+ nutritious recipes, beautiful photos, beginner-friendly.',
            'price': 2499,
            'image_url': 'https://images.unsplash.com/photo-1588561299957-a5b5f1e2f50e?w=400&h=400&fit=crop',
            'category': 'Books',
            'stock': 75,
            'featured': False
        },
        {
            'name': 'Journal Leather Bound',
            'description': 'Thick paper, ribbon bookmark, elegant design. Record your thoughts.',
            'price': 1999,
            'image_url': 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&h=400&fit=crop',
            'category': 'Books',
            'stock': 85,
            'featured': False
        },
        {
            'name': 'Notebook Set (3)',
            'description': 'Lined pages, durable covers, perfect size. Great for notes and sketches.',
            'price': 1299,
            'image_url': 'https://images.unsplash.com/photo-1517842645767-c639042777db?w=400&h=400&fit=crop',
            'category': 'Books',
            'stock': 120,
            'featured': False
        },
        
        # BEAUTY & PERSONAL CARE
        {
            'name': 'Electric Toothbrush',
            'description': 'Sonic technology, multiple modes, long battery life. Dental health made easy.',
            'price': 7999,
            'image_url': 'https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=400&h=400&fit=crop',
            'category': 'Beauty',
            'stock': 55,
            'featured': True
        },
        {
            'name': 'Hair Dryer Professional',
            'description': 'Ionic technology, multiple heat settings, lightweight. Salon results at home.',
            'price': 6999,
            'image_url': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=400&h=400&fit=crop',
            'category': 'Beauty',
            'stock': 40,
            'featured': False
        },
        {
            'name': 'Skincare Set',
            'description': 'Cleanser, toner, moisturizer. Complete daily routine for healthy skin.',
            'price': 4999,
            'image_url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&h=400&fit=crop',
            'category': 'Beauty',
            'stock': 60,
            'featured': True
        },
        {
            'name': 'Makeup Brush Set',
            'description': 'Professional quality, soft bristles, complete set. Flawless application.',
            'price': 3999,
            'image_url': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop',
            'category': 'Beauty',
            'stock': 70,
            'featured': False
        },
        {
            'name': 'Perfume Gift Set',
            'description': 'Elegant fragrance, long-lasting, beautiful packaging. Perfect gift.',
            'price': 8999,
            'image_url': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=400&fit=crop',
            'category': 'Beauty',
            'stock': 45,
            'featured': False
        },
        {
            'name': 'Face Masks Pack (10)',
            'description': 'Hydrating, various types, natural ingredients. Spa day at home.',
            'price': 1999,
            'image_url': 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400&h=400&fit=crop',
            'category': 'Beauty',
            'stock': 100,
            'featured': False
        },
        
        # MORE ELECTRONICS
        {
            'name': 'Portable Charger 20000mAh',
            'description': 'Fast charging, multiple devices, LED display. Never run out of battery.',
            'price': 4999,
            'image_url': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 80,
            'featured': False
        },
        {
            'name': 'Phone Case Leather',
            'description': 'Premium leather, card slots, magnetic closure. Protection meets style.',
            'price': 2999,
            'image_url': 'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 200,
            'featured': False
        },
        {
            'name': 'Screen Protector Pack',
            'description': 'Tempered glass, bubble-free, case-friendly. Ultimate screen protection.',
            'price': 999,
            'image_url': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 250,
            'featured': False
        },
        {
            'name': 'Tablet Stand Adjustable',
            'description': 'Multi-angle, stable base, portable. Perfect for watching and reading.',
            'price': 1999,
            'image_url': 'https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 90,
            'featured': False
        },
        {
            'name': 'HDMI Cable 6ft',
            'description': '4K support, high-speed, gold-plated connectors. Crystal clear video.',
            'price': 1499,
            'image_url': 'https://images.unsplash.com/photo-1625281493651-ddcae3e17e13?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 150,
            'featured': False
        },
        {
            'name': 'Ring Light LED',
            'description': 'Adjustable brightness, phone holder, tripod included. Perfect lighting.',
            'price': 5999,
            'image_url': 'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 55,
            'featured': False
        },
        {
            'name': 'Microphone USB',
            'description': 'Studio quality, plug and play, adjustable stand. Clear recordings.',
            'price': 7999,
            'image_url': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=400&h=400&fit=crop',
            'category': 'Electronics',
            'stock': 45,
            'featured': False
        },
        
        # MORE HOME ITEMS
        {
            'name': 'Candle Set Aromatherapy',
            'description': 'Natural soy wax, relaxing scents, long burn time. Create ambiance.',
            'price': 2999,
            'image_url': 'https://images.unsplash.com/photo-1602874801006-40b46945f6a8?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 95,
            'featured': False
        },
        {
            'name': 'Picture Frame Set',
            'description': 'Various sizes, quality glass, easy hanging. Display your memories.',
            'price': 3499,
            'image_url': 'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 75,
            'featured': False
        },
        {
            'name': 'Kitchen Knife Set',
            'description': 'Professional grade, sharp blades, wooden block. Essential cooking tools.',
            'price': 9999,
            'image_url': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 40,
            'featured': False
        },
        {
            'name': 'Cutting Board Bamboo',
            'description': 'Eco-friendly, knife-friendly, easy to clean. Durable and sustainable.',
            'price': 2499,
            'image_url': 'https://images.unsplash.com/photo-1608022014989-e666cda59d31?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 85,
            'featured': False
        },
        {
            'name': 'Storage Bins Set (3)',
            'description': 'Collapsible, handles, versatile. Organize your space effortlessly.',
            'price': 2999,
            'image_url': 'https://images.unsplash.com/photo-1600096194534-95cf5ece04cf?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 100,
            'featured': False
        },
        {
            'name': 'Wall Clock Modern',
            'description': 'Silent mechanism, easy to read, stylish design. Time in style.',
            'price': 3999,
            'image_url': 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 65,
            'featured': False
        },
        {
            'name': 'Door Mat Welcome',
            'description': 'Durable, weather-resistant, attractive design. Great first impression.',
            'price': 1999,
            'image_url': 'https://images.unsplash.com/photo-1581974206766-2191e34b1e2e?w=400&h=400&fit=crop',
            'category': 'Home & Garden',
            'stock': 110,
            'featured': False
        }
    ]
    
    for product_data in sample_products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
    print(f"Loaded {len(sample_products)} sample products across multiple categories!")

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
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'store.db')
    if not os.path.exists(db_path):
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