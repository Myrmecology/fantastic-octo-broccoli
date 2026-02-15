# ========================================
# JUSTIN E-COMMERCE - Configuration
# ========================================

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # ============ FLASK SETTINGS ============
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # ============ SERVER SETTINGS ============
    HOST = os.getenv('HOST', 'localhost')
    PORT = int(os.getenv('PORT', 5001))
    
    # ============ DATABASE ============
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database/store.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # ============ SESSION ============
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'justin_ecommerce_'
    
    # ============ STRIPE ============
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_CURRENCY = 'usd'
    
    # ============ EMAIL ============
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'store@justinecommerce.com')
    
    # ============ STORE INFO ============
    STORE_NAME = 'JUSTIN E-COMMERCE'
    STORE_TAGLINE = 'Sit back and enjoy an easy to use site for all your shopping needs'
    
    # ============ QUANTUM PROJECT ============
    QUANTUM_URL = os.getenv('QUANTUM_URL', 'http://localhost:5000')
    
    # ============ UPLOAD SETTINGS ============
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # ============ PRICING ============
    TAX_RATE = 0.0825  # 8.25% sales tax
    SHIPPING_COST = 999  # $9.99 in cents
    CURRENCY_SYMBOL = '$'

# ========================================
# END OF CONFIGURATION
# ========================================