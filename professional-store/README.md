# JUSTIN E-COMMERCE - Professional Store

A modern, production-ready e-commerce platform with real payment processing, database persistence, and a stunning user interface.

## 🎯 Overview

This is a professional e-commerce store that runs alongside the Quantum Job Search project. It features:

- ✅ Real Stripe payment processing (test mode)
- ✅ Database-backed product catalog and orders
- ✅ Email confirmations via SendGrid
- ✅ Modern glass morphism design
- ✅ Blue, silver, and dark crimson color scheme
- ✅ Seamless navigation to/from Quantum project

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Stripe account (for payments)
- SendGrid account (for emails)

### Installation

1. **Navigate to the professional store directory:**
```bash
   cd FANTASTIC-OCTO-BROCCOLI/professional-store
```

2. **Install Python dependencies:**
```bash
   pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env and add your API keys
   nano .env
```

4. **Initialize the database:**
```bash
   python app.py
```
   This will create the database and load sample products.

5. **Run the server:**
```bash
   python app.py
```
   Server will start on `http://localhost:5001`

## 🔑 Environment Variables

Edit `.env` file with your credentials:
```env
# Flask
SECRET_KEY=your-super-secret-key-change-this

# Stripe (get from https://dashboard.stripe.com/test/apikeys)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# SendGrid (get from https://app.sendgrid.com/settings/api_keys)
SENDGRID_API_KEY=SG....
FROM_EMAIL=store@justinecommerce.com

# Quantum Project
QUANTUM_URL=http://localhost:5000
```

## 📁 Project Structure
```
professional-store/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not committed)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules (YubiKey secure)
├── README.md                  # This file
│
├── database/
│   ├── __init__.py
│   ├── schema.sql             # Database schema
│   └── store.db              # SQLite database (auto-generated)
│
├── models/
│   ├── __init__.py
│   ├── product.py            # Product model
│   ├── order.py              # Order & OrderItem models
│   └── user.py               # User & Cart models
│
├── routes/
│   ├── __init__.py
│   ├── store.py              # Store routes (products, catalog)
│   ├── cart.py               # Shopping cart routes
│   └── checkout.py           # Checkout & payment routes
│
├── templates/
│   ├── base.html             # Base template (navigation)
│   ├── landing.html          # Landing page (JUSTIN E-COMMERCE splash)
│   ├── store.html            # Product catalog
│   ├── product.html          # Product details
│   ├── cart.html             # Shopping cart
│   ├── checkout.html         # Checkout page
│   └── confirmation.html     # Order confirmation
│
└── static/
    ├── css/
    │   ├── main.css          # Main styles
    │   ├── landing.css       # Landing page styles
    │   └── components.css    # Component styles
    ├── js/
    │   ├── main.js           # Main JavaScript
    │   ├── cart.js           # Cart functionality
    │   └── animations.js     # Visual effects
    └── images/
        └── hero-background.jpg  # Landing page background
```

## 🌐 Running Both Projects

### Terminal 1: Quantum Project (Port 5000)
```bash
cd FANTASTIC-OCTO-BROCCOLI
python quantumServer_ecommerce.py
```

### Terminal 2: Professional Store (Port 5001)
```bash
cd FANTASTIC-OCTO-BROCCOLI/professional-store
python app.py
```

### Navigation Flow
1. Visit `http://localhost:5000` (Quantum fractals)
2. Click "Visit Store" → Quantum demo store
3. Click "Enter Professional Store →" → `http://localhost:5001`
4. See JUSTIN E-COMMERCE landing page
5. Click "← Back to Quantum Home" → Returns to `http://localhost:5000`

## 💳 Payment Testing

Use Stripe test cards:

| Card Number         | Result          |
|---------------------|-----------------|
| 4242 4242 4242 4242 | Success         |
| 4000 0000 0000 0002 | Decline         |
| 4000 0027 6000 3184 | 3D Secure auth  |

- **Expiry:** Any future date
- **CVC:** Any 3 digits
- **ZIP:** Any 5 digits

## 📧 Email Configuration

### SendGrid Setup
1. Create account at https://sendgrid.com
2. Generate API key
3. Add to `.env` file
4. Verify sender email

### Email Templates
- Order confirmation (sent automatically after purchase)
- Includes order details, items, shipping address

## 🗄️ Database

### SQLite (Development)
- File: `database/store.db`
- Auto-created on first run
- Includes sample products

### Tables
- **products** - Product catalog
- **orders** - Customer orders
- **order_items** - Order line items
- **cart** - Shopping cart (session-based)
- **users** - Customer information

### Sample Data
8 sample products are loaded automatically:
- Premium Headphones ($299.99)
- Smart Watch ($399.99)
- Laptop Stand ($49.99)
- Mechanical Keyboard ($149.99)
- And more...

## 🎨 Design System

### Color Palette
```css
/* Blues */
--midnight-blue: #0f1c2e;
--ocean-blue: #1e3a5f;
--bright-blue: #4a90e2;
--electric-blue: #5dade2;

/* Silvers */
--silver-light: #c0c5ce;
--silver: #a8adb5;
--chrome: #e8eaed;

/* Crimsons */
--dark-crimson: #8b0000;
--crimson: #a52a2a;
```

### Features
- Glass morphism effects
- Frosted search bars
- Floating cart animations
- Smooth transitions
- Responsive design

## 🛠️ Development

### Adding Products
```python
from models import db, Product

product = Product(
    name="New Product",
    description="Product description",
    price=4999,  # $49.99 in cents
    category="Electronics",
    stock=100,
    featured=True
)
db.session.add(product)
db.session.commit()
```

### Running Migrations
```bash
# If you modify models, recreate database
rm database/store.db
python app.py
```

## 🔒 Security

### Features
- Secure .gitignore (includes YubiKey protection)
- Environment variables for secrets
- CSRF protection
- Secure sessions
- Stripe PCI compliance

### Never Commit
- `.env` file
- `database/store.db`
- API keys
- Customer data

## 📊 API Endpoints

### Store
- `GET /` - Landing page
- `GET /store` - Product catalog
- `GET /product/<id>` - Product details
- `GET /api/products` - Products JSON

### Cart
- `POST /cart/add` - Add to cart
- `POST /cart/update` - Update quantity
- `POST /cart/remove/<id>` - Remove item
- `GET /cart` - View cart

### Checkout
- `GET /checkout` - Checkout page
- `POST /create-payment-intent` - Create Stripe payment
- `POST /process-order` - Process order
- `GET /confirmation/<order_number>` - Order confirmation

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm database/store.db
python app.py
```

### Port Already in Use
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9
```

### Stripe Errors
- Check API keys in `.env`
- Ensure test mode keys (pk_test_... and sk_test_...)
- Verify publishable key matches secret key

### Email Not Sending
- Check SendGrid API key
- Verify sender email
- Check SendGrid dashboard for errors

## 📝 Mission Statement

> "Welcome to JUSTIN E-COMMERCE. Sit back and enjoy an easy to use site for all your shopping needs. If you feel like you can't afford it, that's okay. JUSTIN E-COMMERCE is here to make you go broke. The more you spend, the richer I get." 💰

## 🎯 Features Checklist

- ✅ Landing page with glass morphism design
- ✅ Product catalog with search and filters
- ✅ Shopping cart with session persistence
- ✅ Real Stripe payment processing
- ✅ Order confirmation emails
- ✅ Database-backed orders
- ✅ Navigation to/from Quantum project
- ✅ Mobile responsive design
- ✅ Professional UI/UX



## 📄 License

Part of the FANTASTIC-OCTO-BROCCOLI project.

---

**Built with ❤️ using Flask, Stripe, and SendGrid**

**Last Updated:** February 2026