# ========================================
# JUSTIN E-COMMERCE - User Model
# ========================================

from datetime import datetime
from models import db

class User(db.Model):
    """User model - Currently minimal for guest checkout"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    name = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Cart(db.Model):
    """Shopping cart model - session-based"""
    
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to product
    product = db.relationship('Product', backref='cart_items')
    
    def __repr__(self):
        return f'<Cart {self.session_id} - Product {self.product_id}>'
    
    def to_dict(self):
        """Convert cart item to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'subtotal': self.get_subtotal(),
            'subtotal_formatted': f"${self.get_subtotal() / 100:.2f}"
        }
    
    def get_subtotal(self):
        """Calculate subtotal for this cart item"""
        if self.product:
            return self.product.price * self.quantity
        return 0

# ========================================
# END OF USER MODEL
# ========================================