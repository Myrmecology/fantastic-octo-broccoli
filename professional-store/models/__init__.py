# ========================================
# JUSTIN E-COMMERCE - Models Package
# ========================================

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Import all models
from models.product import Product
from models.order import Order, OrderItem
from models.user import User, Cart

# Export all models
__all__ = [
    'db',
    'Product',
    'Order',
    'OrderItem',
    'User',
    'Cart'
]

# ========================================
# END OF MODELS INIT
# ========================================