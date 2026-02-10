# Quantum Job Search + E-Commerce

A multi-page web application powered by real quantum physics simulations. Features job search with WebGL fractals and a fully functional e-commerce store.

## Features

- 🌌 Quantum job search with real-time fractal visualization
- 🔬 Toggle between Artistic and Scientific modes
- 🛒 E-commerce store with quantum-generated pricing
- 📊 Real-time stats overlay showing quantum metrics
- 🧮 Schrödinger equation solver integration
- 🎨 Product catalog, cart, and checkout system

## Quick Start

### Install Dependencies
```bash
pip install flask flask-cors numpy
```

### Run Server
```bash
python quantumServer_ecommerce.py
```

### Access Pages
- Homepage: http://localhost:5000
- Store: http://localhost:5000/store
- Cart: http://localhost:5000/cart
- Checkout: http://localhost:5000/checkout

## Project Structure
```
FANTASTIC-OCTO-BROCCOLI/
├── quantumServer_ecommerce.py    # Backend server
├── templates/                     # HTML pages
│   ├── home.html                 # Quantum job search
│   ├── store.html                # Product catalog
│   ├── product.html              # Product details
│   ├── cart.html                 # Shopping cart
│   └── checkout.html             # Checkout page
├── static/                        # Assets (CSS/JS)
└── README.md
```

## How It Works

- **Quantum Simulation**: Real Schrödinger equation solver powers the visual effects
- **Dynamic Pricing**: Product prices influenced by quantum entropy values
- **Multi-Page**: Flask routes handle navigation between pages
- **Session Management**: Shopping cart persists across pages

## Tech Stack

- Python + Flask
- NumPy for quantum mechanics
- WebGL for 3D fractals
- Vanilla JavaScript (no frameworks)
