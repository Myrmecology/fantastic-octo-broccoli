# ========================================
# JUSTIN E-COMMERCE - Order Model
# ========================================

from datetime import datetime
from models import db
import secrets
import string

class Order(db.Model):
    """Order model for customer purchases"""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(20))
    shipping_address = db.Column(db.String(500))
    shipping_city = db.Column(db.String(100))
    shipping_state = db.Column(db.String(50))
    shipping_zip = db.Column(db.String(20))
    subtotal = db.Column(db.Integer, nullable=False)  # In cents
    tax = db.Column(db.Integer, nullable=False)  # In cents
    shipping = db.Column(db.Integer, nullable=False)  # In cents
    total = db.Column(db.Integer, nullable=False)  # In cents
    status = db.Column(db.String(50), default='pending')
    stripe_payment_id = db.Column(db.String(200))
    stripe_payment_status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to order items
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number (e.g., JE-ABC123XYZ)"""
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(secrets.choice(chars) for _ in range(9))
        return f"JE-{random_part}"
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'shipping_address': self.shipping_address,
            'shipping_city': self.shipping_city,
            'shipping_state': self.shipping_state,
            'shipping_zip': self.shipping_zip,
            'subtotal': self.subtotal,
            'subtotal_formatted': f"${self.subtotal / 100:.2f}",
            'tax': self.tax,
            'tax_formatted': f"${self.tax / 100:.2f}",
            'shipping': self.shipping,
            'shipping_formatted': f"${self.shipping / 100:.2f}",
            'total': self.total,
            'total_formatted': f"${self.total / 100:.2f}",
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items]
        }
    
    def get_full_address(self):
        """Get formatted full shipping address"""
        parts = [
            self.shipping_address,
            f"{self.shipping_city}, {self.shipping_state} {self.shipping_zip}"
        ]
        return '\n'.join(filter(None, parts))


class OrderItem(db.Model):
    """Order item model for individual products in an order"""
    
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Price per item in cents
    subtotal = db.Column(db.Integer, nullable=False)  # quantity * price in cents
    
    def __repr__(self):
        return f'<OrderItem {self.product_name} x{self.quantity}>'
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price': self.price,
            'price_formatted': f"${self.price / 100:.2f}",
            'subtotal': self.subtotal,
            'subtotal_formatted': f"${self.subtotal / 100:.2f}"
        }

# ========================================
# END OF ORDER MODEL
# ========================================