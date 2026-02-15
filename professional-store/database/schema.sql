-- ========================================
-- JUSTIN E-COMMERCE - Database Schema
-- ========================================

-- ============ PRODUCTS TABLE ============
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,              -- Price in cents (e.g., 2999 = $29.99)
    image_url TEXT,
    category TEXT,
    stock INTEGER DEFAULT 0,
    featured BOOLEAN DEFAULT 0,
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ ORDERS TABLE ============
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_phone TEXT,
    shipping_address TEXT,
    shipping_city TEXT,
    shipping_state TEXT,
    shipping_zip TEXT,
    subtotal INTEGER NOT NULL,           -- Subtotal in cents
    tax INTEGER NOT NULL,                -- Tax in cents
    shipping INTEGER NOT NULL,           -- Shipping in cents
    total INTEGER NOT NULL,              -- Total in cents
    status TEXT DEFAULT 'pending',       -- pending, processing, shipped, delivered, cancelled
    stripe_payment_id TEXT,
    stripe_payment_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============ ORDER ITEMS TABLE ============
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,          -- Store name at time of order
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL,              -- Price per item in cents (at time of order)
    subtotal INTEGER NOT NULL,           -- quantity * price
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ============ CART TABLE (Session-based) ============
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ============ INDEXES FOR PERFORMANCE ============
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(active);
CREATE INDEX IF NOT EXISTS idx_orders_email ON orders(customer_email);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_cart_session ON cart(session_id);

-- ============ SAMPLE PRODUCTS ============
INSERT INTO products (name, description, price, image_url, category, stock, featured) VALUES
('Premium Headphones', 'High-quality wireless headphones with noise cancellation', 29999, '/static/images/products/headphones.jpg', 'Electronics', 50, 1),
('Smart Watch', 'Advanced fitness tracking and notifications', 39999, '/static/images/products/smartwatch.jpg', 'Electronics', 30, 1),
('Laptop Stand', 'Ergonomic aluminum laptop stand', 4999, '/static/images/products/laptop-stand.jpg', 'Accessories', 100, 0),
('Mechanical Keyboard', 'RGB mechanical gaming keyboard', 14999, '/static/images/products/keyboard.jpg', 'Electronics', 25, 1),
('Wireless Mouse', 'Precision wireless gaming mouse', 7999, '/static/images/products/mouse.jpg', 'Electronics', 75, 0),
('USB-C Hub', '7-in-1 USB-C hub for laptops', 5999, '/static/images/products/usb-hub.jpg', 'Accessories', 60, 0),
('Phone Case', 'Premium leather phone case', 3999, '/static/images/products/phone-case.jpg', 'Accessories', 200, 0),
('Portable Charger', '20000mAh fast charging power bank', 4999, '/static/images/products/charger.jpg', 'Electronics', 80, 0);

-- ========================================
-- END OF SCHEMA
-- Database ready for JUSTIN E-COMMERCE
-- ========================================