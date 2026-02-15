# ========================================
# JUSTIN E-COMMERCE - Product Model
# ========================================

from datetime import datetime
from models import db

class Product(db.Model):
    """Product model for store items"""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)  # Price in cents
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'price_formatted': self.get_price_formatted(),
            'image_url': self.image_url,
            'category': self.category,
            'stock': self.stock,
            'featured': self.featured,
            'active': self.active,
            'in_stock': self.is_in_stock(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_price_formatted(self):
        """Get price formatted as currency (e.g., $29.99)"""
        return f"${self.price / 100:.2f}"
    
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0
    
    def reduce_stock(self, quantity):
        """Reduce stock by quantity"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

# ========================================
# END OF PRODUCT MODEL
# ========================================