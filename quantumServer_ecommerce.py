"""
Quantum Job Search + E-Commerce Server
Multi-page application with store functionality
"""

from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
import math, random, cmath, time
import secrets

# NumPy for real quantum mechanics
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# ---------------------------
# EXISTING Quantum Code (UNCHANGED)
# ---------------------------
HBAR = 1.0
KB = 1.0
TEMP = 0.7

def normalize(vec):
    n = math.sqrt(sum(abs(x)**2 for x in vec))
    return [x / n for x in vec]

class QuantumState:
    def __init__(self, dim):
        self.dim = dim
        self.psi = normalize([
            complex(random.random(), random.random())
            for _ in range(dim)
        ])

    def evolve(self, hamiltonian, dt):
        new = []
        for i in range(self.dim):
            amp = sum(hamiltonian[i][j] * self.psi[j]
                      for j in range(self.dim))
            new.append(self.psi[i] - 1j * amp * dt / HBAR)
        self.psi = normalize(new)

    def measure(self):
        probs = [abs(a)**2 for a in self.psi]
        r, acc = random.random(), 0.0
        for i, p in enumerate(probs):
            acc += p
            if r <= acc:
                return i

class Multiverse:
    def __init__(self, state):
        self.branches = [state]

    def branch(self):
        new = []
        for s in self.branches:
            for _ in range(2):
                c = QuantumState(s.dim)
                c.psi = s.psi[:]
                new.append(c)
        self.branches = new

def potential(x):
    return x**4 - x**2

def tunneling(E, barrier):
    if E >= barrier:
        return 1.0
    return math.exp(-2 * math.sqrt(barrier - E) / HBAR)

def bio_efficiency(coherence_time):
    decoherence = math.exp(-1 / coherence_time)
    thermal_noise = math.exp(-TEMP / KB)
    return decoherence * thermal_noise

def random_hamiltonian(dim):
    H = [[0]*dim for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            H[i][j] = random.random() if i == j else 0.0
    return H

JOB_PREFIXES = [
    "Quantum", "Neural", "Interdimensional", "Hyperbolic", 
    "Fractal", "Chaotic", "Entropic", "Holographic",
    "Recursive", "Asymptotic", "Stochastic", "Chromatic"
]

JOB_ROLES = [
    "UX Designer", "Backend Wizard", "Data Shaman", "Code Poet",
    "Reality Engineer", "Probability Architect", "Loop Master",
    "Stack Weaver", "API Mystic", "Cloud Shepherd"
]

def generate_quantum_job(quantum_value):
    prefix_idx = int(quantum_value * len(JOB_PREFIXES)) % len(JOB_PREFIXES)
    role_idx = int((quantum_value * 1000) % len(JOB_ROLES))
    return f"{JOB_PREFIXES[prefix_idx]} {JOB_ROLES[role_idx]}"

# ---------------------------
# Schrödinger Solver (UNCHANGED)
# ---------------------------
class SchrodingerSolver:
    def __init__(self, Nx=200, x_range=(-10, 10)):
        if not NUMPY_AVAILABLE:
            raise RuntimeError("NumPy required")
        
        self.Nx = Nx
        self.x = np.linspace(x_range[0], x_range[1], Nx)
        self.dx = self.x[1] - self.x[0]
        self.hbar = 1.0
        self.m = 1.0
        
        x0 = -3
        k0 = 5
        self.psi = np.exp(-(self.x - x0)**2) * np.exp(1j * k0 * self.x)
        self.psi /= np.sqrt(np.sum(np.abs(self.psi)**2) * self.dx)
        
        self._build_hamiltonian()
    
    def _build_hamiltonian(self):
        laplacian = (
            -2 * np.eye(self.Nx)
            + np.eye(self.Nx, k=1)
            + np.eye(self.Nx, k=-1)
        ) / self.dx**2
        V = np.zeros(self.Nx)
        self.H = -(self.hbar**2 / (2 * self.m)) * laplacian + np.diag(V)
    
    def evolve(self, steps=100, dt=0.001):
        start_time = time.time()
        for _ in range(steps):
            self.psi += -1j * dt / self.hbar * (self.H @ self.psi)
            self.psi /= np.sqrt(np.sum(np.abs(self.psi)**2) * self.dx)
        return time.time() - start_time
    
    def get_wavefunction_data(self):
        prob_density = np.abs(self.psi)**2
        return {
            'x': self.x.tolist(),
            'probability': prob_density.tolist(),
            'real': np.real(self.psi).tolist(),
            'imag': np.imag(self.psi).tolist(),
        }

# ---------------------------
# NEW: Product Data
# ---------------------------
PRODUCTS = [
    # Original Quantum Products (1-6)
    {
        'id': 1,
        'name': 'Quantum Coding Masterclass',
        'category': 'course',
        'base_price': 299,
        'description': 'Learn to code across infinite universes simultaneously',
        'features': ['12 hours of quantum content', 'Certificate from all timelines', 'Access to multiverse mentors'],
        'image': '🎓'
    },
    {
        'id': 2,
        'name': 'Schrödinger Solver Pro License',
        'category': 'software',
        'base_price': 499,
        'description': 'Production-grade quantum wavefunction solver',
        'features': ['Real-time evolution', 'Multi-dimensional support', 'C++/Rust bindings'],
        'image': '⚛️'
    },
    {
        'id': 3,
        'name': 'Fractal Shader Pack',
        'category': 'asset',
        'base_price': 149,
        'description': 'Premium WebGL fractal collection',
        'features': ['50+ fractals', 'Customizable parameters', 'Performance optimized'],
        'image': '🌀'
    },
    {
        'id': 4,
        'name': 'Multiverse Analytics Dashboard',
        'category': 'tool',
        'base_price': 799,
        'description': 'Track metrics across parallel universes',
        'features': ['Real-time branching', 'Infinite scalability', 'Quantum-encrypted'],
        'image': '📊'
    },
    {
        'id': 5,
        'name': 'Neural Network Training Pod',
        'category': 'service',
        'base_price': 1999,
        'description': 'Quantum-accelerated AI model training',
        'features': ['100x speedup', 'Superposition training', 'Entangled gradients'],
        'image': '🧠'
    },
    {
        'id': 6,
        'name': 'Interdimensional API Access',
        'category': 'api',
        'base_price': 99,
        'description': 'Connect to quantum APIs across realities',
        'features': ['Unlimited requests', '99.99% uptime (per universe)', 'WebSocket support'],
        'image': '🔌'
    },
    
    # NEW Products (7-37)
    {
        'id': 7,
        'name': 'Alabama Ball Cap',
        'category': 'apparel',
        'base_price': 29,
        'description': 'Classic crimson ball cap with quantum-stitched logo',
        'features': ['Adjustable fit', 'Breathable fabric', 'Roll Tide in all dimensions'],
        'image': '🧢'
    },
    {
        'id': 8,
        'name': 'Custom Logo T-Shirt',
        'category': 'apparel',
        'base_price': 24,
        'description': 'Personalized t-shirt with your logo printed across infinite timelines',
        'features': ['100% cotton', 'Custom design', 'Quantum-fade resistant'],
        'image': '👕'
    },
    {
        'id': 9,
        'name': 'Harvard University Hoodie',
        'category': 'apparel',
        'base_price': 68,
        'description': 'Premium crimson hoodie from the multiverse\'s finest university',
        'features': ['Officially licensed', 'Fleece-lined', 'Veritas across all realities'],
        'image': '🧥'
    },
    {
        'id': 10,
        'name': 'Brown University Hoodie',
        'category': 'apparel',
        'base_price': 65,
        'description': 'Comfortable Brown University hoodie with quantum warmth technology',
        'features': ['Super soft fleece', 'Kangaroo pocket', 'Bruno the Bear approved'],
        'image': '🧥'
    },
    {
        'id': 11,
        'name': 'Princeton University T-Shirt',
        'category': 'apparel',
        'base_price': 32,
        'description': 'Classic orange and black tee from the Garden State\'s pride',
        'features': ['Pre-shrunk fabric', 'Tiger mascot design', 'Ivy League certified'],
        'image': '👕'
    },
    {
        'id': 12,
        'name': 'Yale University Sweatshirt',
        'category': 'apparel',
        'base_price': 58,
        'description': 'Traditional Yale blue crew neck sweatshirt',
        'features': ['Ribbed cuffs', 'Lux et Veritas embroidered', 'Handsome Dan edition'],
        'image': '👔'
    },
    {
        'id': 13,
        'name': 'Cambridge University Hoodie',
        'category': 'apparel',
        'base_price': 72,
        'description': 'Distinguished Cambridge light blue hoodie from across the pond',
        'features': ['British quality', 'Boat race ready', 'Quantum rowing approved'],
        'image': '🧥'
    },
    {
        'id': 14,
        'name': 'Stanford University Hoodie',
        'category': 'apparel',
        'base_price': 70,
        'description': 'Cardinal red hoodie from Silicon Valley\'s academic powerhouse',
        'features': ['Innovation guaranteed', 'Tree mascot pride', 'Startup founder approved'],
        'image': '🧥'
    },
    {
        'id': 15,
        'name': 'Silver Pine State University Hoodie',
        'category': 'apparel',
        'base_price': 55,
        'description': 'Exclusive Silver Pine State hoodie - show your school spirit!',
        'features': ['Limited edition', 'Campus exclusive', 'Go Timber Wolves!'],
        'image': '🧥'
    },
    {
        'id': 16,
        'name': 'Silver Pine State University Ball Cap',
        'category': 'apparel',
        'base_price': 25,
        'description': 'Rep your Silver Pine State pride with this classic cap',
        'features': ['Embroidered logo', 'Curved brim', 'Alumni approved'],
        'image': '🧢'
    },
    {
        'id': 17,
        'name': 'Silver Pine State University Water Bottle',
        'category': 'item',
        'base_price': 18,
        'description': 'Stay hydrated across all dimensions with official SPSU gear',
        'features': ['32 oz capacity', 'BPA-free', 'Quantum insulation'],
        'image': '💧'
    },
    {
        'id': 18,
        'name': 'Refurbished Sega Saturn',
        'category': 'electronics',
        'base_price': 249,
        'description': 'Fully restored Sega Saturn console - relive the 90s in any universe',
        'features': ['Tested and working', 'Includes controller', 'Plays across timelines'],
        'image': '🎮'
    },
    {
        'id': 19,
        'name': 'Encyclopedia Of Calculus',
        'category': 'book',
        'base_price': 89,
        'description': 'Comprehensive guide to calculus across infinite mathematical dimensions',
        'features': ['1200 pages', 'All theorems included', 'Limit does not exist'],
        'image': '📚'
    },
    {
        'id': 20,
        'name': 'Introduction to Molecular Biology',
        'category': 'book',
        'base_price': 125,
        'description': 'Essential textbook for understanding life at the molecular level',
        'features': ['Latest edition', 'Full-color diagrams', 'DNA helix poster included'],
        'image': '📖'
    },
    {
        'id': 21,
        'name': 'Linear Algebra',
        'category': 'book',
        'base_price': 95,
        'description': 'Master vectors, matrices, and transformations in n-dimensional space',
        'features': ['Proof-based approach', '500+ exercises', 'Eigenvalue guaranteed'],
        'image': '📕'
    },
    {
        'id': 22,
        'name': '200 Inch Television',
        'category': 'electronics',
        'base_price': 8999,
        'description': 'Massive 200-inch 8K display - your living room becomes a theater',
        'features': ['8K resolution', 'HDR support', 'Multiverse streaming ready'],
        'image': '📺'
    },
    {
        'id': 23,
        'name': '400 Inch Television',
        'category': 'electronics',
        'base_price': 24999,
        'description': 'Absurdly large 400-inch display - why not?',
        'features': ['16K resolution', 'Requires reinforced wall', 'Visible from space'],
        'image': '📺'
    },
    {
        'id': 24,
        'name': '2000 Inch Projection Screen',
        'category': 'electronics',
        'base_price': 4500,
        'description': 'Commercial-grade projection screen for truly epic viewing',
        'features': ['Motorized retractable', 'Matte white surface', 'IMAX at home'],
        'image': '🎬'
    },
    {
        'id': 25,
        'name': 'Box Of Bubble Gum',
        'category': 'item',
        'base_price': 6,
        'description': 'Classic bubble gum - 50 pieces of chewy quantum goodness',
        'features': ['Sugar-free option', '50 pieces', 'Bubbles in any dimension'],
        'image': '🍬'
    },
    {
        'id': 26,
        'name': 'Ethical Hacking Guide',
        'category': 'book',
        'base_price': 49,
        'description': 'Learn penetration testing and security auditing the right way',
        'features': ['Hands-on labs', 'Legal framework', 'Bug bounty tips'],
        'image': '🔐'
    },
    {
        'id': 27,
        'name': '2002 Isuzu Trooper (Perfect Condition)',
        'category': 'vehicle',
        'base_price': 8500,
        'description': 'Mint condition Isuzu Trooper - adventure ready across all timelines',
        'features': ['4WD capability', '120k miles', 'Quantum rust-proofed'],
        'image': '🚙'
    },
    {
        'id': 28,
        'name': 'Mystery Box',
        'category': 'item',
        'base_price': 99,
        'description': 'Contains something from a random parallel universe - total surprise!',
        'features': ['Unknown contents', 'Guaranteed value', 'Schrödinger approved'],
        'image': '📦'
    },
    {
        'id': 29,
        'name': 'Strawberry Ice Cream',
        'category': 'item',
        'base_price': 8,
        'description': 'Premium strawberry ice cream - one pint of frozen quantum bliss',
        'features': ['Real strawberries', 'Hand-churned', 'Exists in superposition until opened'],
        'image': '🍨'
    },
    {
        'id': 30,
        'name': 'Floor Lamp',
        'category': 'item',
        'base_price': 45,
        'description': 'Modern LED floor lamp with adjustable brightness',
        'features': ['Touch control', '3 brightness levels', 'Illuminates all dimensions'],
        'image': '💡'
    },
    {
        'id': 31,
        'name': 'Computer Desk',
        'category': 'item',
        'base_price': 199,
        'description': 'Ergonomic L-shaped computer desk with cable management',
        'features': ['Spacious surface', 'Cable grommets', 'Quantum workspace optimized'],
        'image': '🪑'
    },
    {
        'id': 32,
        'name': 'Just Cause 2 Video Game',
        'category': 'electronics',
        'base_price': 15,
        'description': 'Classic open-world action game - chaos across parallel Panaus',
        'features': ['PC digital code', 'Grappling hook included', 'Unlimited explosions'],
        'image': '🎮'
    },
    {
        'id': 33,
        'name': 'Alternate Reality Vacation Package',
        'category': 'experience',
        'base_price': 24999,
        'description': 'Two-week vacation to a parallel universe of your choice',
        'features': ['Reality transport included', 'Hotel accommodations', 'Tour guide assistance'],
        'image': '🌍'
    },
    {
        'id': 34,
        'name': 'Time Traveling Manual',
        'category': 'book',
        'base_price': 499,
        'description': 'Comprehensive guide to temporal navigation and paradox prevention',
        'features': ['Grandfather paradox solutions', 'Timeline repair kit', 'Flux capacitor diagram'],
        'image': '⏰'
    },
    {
        'id': 35,
        'name': '22,000 Inch Television',
        'category': 'electronics',
        'base_price': 999999,
        'description': 'The most ridiculous television ever conceived - nearly 2000 feet diagonal',
        'features': ['Requires stadium', 'Resolution: YES', 'Installation not included'],
        'image': '📺'
    },
    {
        'id': 36,
        'name': 'Brand New 747 Aircraft (Customize Your Jet)',
        'category': 'vehicle',
        'base_price': 350000000,
        'description': 'Boeing 747-8 commercial aircraft - because why not?',
        'features': ['Full customization', 'Pilot training included', 'Flies in all universes'],
        'image': '✈️'
    },
    {
        'id': 37,
        'name': 'A Bottle Of Water',
        'category': 'item',
        'base_price': 3,
        'description': 'Simple 16.9 oz bottle of purified water - hydration is important',
        'features': ['H2O molecules', 'Quantum purified', 'BPA-free bottle'],
        'image': '💧'
    }
]

def generate_quantum_price(base_price):
    """Generate price influenced by quantum state"""
    entropy_factor = random.uniform(0.8, 1.2)
    return int(base_price * entropy_factor)

# ---------------------------
# PAGE ROUTES
# ---------------------------
@app.route('/')
def home():
    """Original quantum job search page"""
    return render_template('home.html')

@app.route('/store')
def store():
    """Product catalog page"""
    return render_template('store.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    """Shopping cart page"""
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    """Checkout page"""
    return render_template('checkout.html')

# ---------------------------
# API ENDPOINTS (ORIGINAL - UNCHANGED)
# ---------------------------
@app.route('/api/quantum-simulation')
def quantum_simulation():
    """ORIGINAL quantum simulation endpoint"""
    DIM = 6
    STEPS = 8
    
    universe = QuantumState(DIM)
    multiverse = Multiverse(universe)
    stats = []
    
    for t in range(STEPS):
        if t % 2 == 0:
            multiverse.branch()
        
        for state in multiverse.branches:
            H = random_hamiltonian(DIM)
            state.evolve(H, dt=0.1)
        
        x = random.uniform(-2, 2)
        E = potential(x)
        T = tunneling(E, barrier=1.0)
        B = bio_efficiency(random.uniform(0.5, 2.5))
        
        entropy = -sum(
            abs(a)**2 * math.log(abs(a)**2 + 1e-9)
            for a in multiverse.branches[0].psi
        )
        
        stats.append({
            'time': t,
            'universes': len(multiverse.branches),
            'energy': E,
            'tunneling': T,
            'efficiency': B,
            'entropy': entropy
        })
    
    jobs = []
    for i in range(4):
        quantum_val = stats[i * 2]['entropy'] + stats[i * 2]['efficiency']
        jobs.append(generate_quantum_job(quantum_val))
    
    visual_params = {
        'fractal_power': 8.0 + stats[-1]['entropy'],
        'color_shift': stats[-1]['tunneling'] * 10,
        'glow_intensity': stats[-1]['efficiency'] * 2,
        'speed_multiplier': 1.0 + stats[-1]['energy'] * 0.5
    }
    
    return jsonify({
        'stats': stats,
        'jobs': jobs,
        'visual': visual_params,
        'total_universes': len(multiverse.branches)
    })

@app.route('/api/search/<query>')
def search_jobs(query):
    """ORIGINAL search endpoint"""
    seed_value = sum(ord(c) for c in query)
    random.seed(seed_value)
    
    DIM = 6
    universe = QuantumState(DIM)
    H = random_hamiltonian(DIM)
    universe.evolve(H, dt=0.5)
    
    entropy = -sum(
        abs(a)**2 * math.log(abs(a)**2 + 1e-9)
        for a in universe.psi
    )
    
    jobs = [generate_quantum_job(entropy + i*0.3) for i in range(5)]
    random.seed()
    
    return jsonify({
        'query': query,
        'jobs': jobs,
        'quantum_entropy': entropy
    })

@app.route('/api/schrodinger-simulation')
def schrodinger_simulation():
    """Real Schrödinger solver endpoint"""
    if not NUMPY_AVAILABLE:
        return jsonify({'error': 'NumPy not installed'}), 500
    
    compilation_start = time.time()
    solver = SchrodingerSolver(Nx=200)
    
    cpp_compile_time = random.uniform(0.2, 0.5)
    schrodinger_time = solver.evolve(steps=300, dt=0.001)
    rust_tasks = random.randint(2, 5)
    rust_compile_time = random.uniform(0.3, 0.7)
    
    total_time = time.time() - compilation_start
    wavefunction_data = solver.get_wavefunction_data()
    
    prob_density = np.array(wavefunction_data['probability'])
    entropy = -np.sum(prob_density * np.log(prob_density + 1e-10)) * solver.dx
    
    x_mean = np.sum(solver.x * prob_density) * solver.dx
    x2_mean = np.sum(solver.x**2 * prob_density) * solver.dx
    delta_x = np.sqrt(x2_mean - x_mean**2)
    
    return jsonify({
        'wavefunction': wavefunction_data,
        'stats': {
            'entropy': float(entropy),
            'position_uncertainty': float(delta_x),
            'steps_per_second': int(300 / schrodinger_time),
            'total_time_ms': float(total_time * 1000),
        },
        'performance': {
            'cpp_compilation_ms': float(cpp_compile_time),
            'schrodinger_compute_ms': float(schrodinger_time * 1000),
            'rust_async_tasks': rust_tasks,
            'rust_compilation_ms': float(rust_compile_time),
        },
        'mode': 'scientific'
    })

# ---------------------------
# NEW: Store API Endpoints
# ---------------------------
@app.route('/api/products')
def get_products():
    """Get all products with quantum-influenced pricing"""
    products_with_prices = []
    for product in PRODUCTS:
        p = product.copy()
        p['price'] = generate_quantum_price(p['base_price'])
        products_with_prices.append(p)
    
    return jsonify({'products': products_with_prices})

@app.route('/api/product/<int:product_id>')
def get_product(product_id):
    """Get single product details"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    p = product.copy()
    p['price'] = generate_quantum_price(p['base_price'])
    return jsonify(p)

@app.route('/api/cart', methods=['GET', 'POST'])
def cart_api():
    """Cart operations"""
    if 'cart' not in session:
        session['cart'] = []
    
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        if action == 'add':
            product_id = data.get('product_id')
            session['cart'].append(product_id)
            session.modified = True
            return jsonify({'success': True, 'cart_count': len(session['cart'])})
        
        elif action == 'remove':
            product_id = data.get('product_id')
            if product_id in session['cart']:
                session['cart'].remove(product_id)
                session.modified = True
            return jsonify({'success': True, 'cart_count': len(session['cart'])})
        
        elif action == 'clear':
            session['cart'] = []
            session.modified = True
            return jsonify({'success': True, 'cart_count': 0})
    
    # GET request - return cart contents
    cart_items = []
    for pid in session['cart']:
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if product:
            p = product.copy()
            p['price'] = generate_quantum_price(p['base_price'])
            cart_items.append(p)
    
    total = sum(item['price'] for item in cart_items)
    
    return jsonify({
        'items': cart_items,
        'count': len(cart_items),
        'total': total
    })

if __name__ == '__main__':
    print("🌌 Quantum Job Search + E-Commerce Server Starting...")
    print("📡 Server running at http://localhost:5000")
    print("🏠 Homepage: http://localhost:5000")
    print("🛒 Store: http://localhost:5000/store")
    if NUMPY_AVAILABLE:
        print("✅ Real Schrödinger solver ENABLED")
    app.run(debug=True, port=5000)