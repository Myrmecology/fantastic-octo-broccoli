# ========================================
# JUSTIN E-COMMERCE - Models Package
# ========================================

from flask_sqlalchemy import SQLAlchemy

# Create single db instance
db = SQLAlchemy()

# Import models (must be after db is created)
from models.product import Product
from models.order import Order, OrderItem
from models.user import User, Cart

# Export all
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