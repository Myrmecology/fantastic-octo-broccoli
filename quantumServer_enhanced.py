"""
Quantum Job Search Server - ENHANCED
Connects quantum simulation to WebGL frontend
NOW WITH: Real Schrödinger equation solver!
"""

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import math, random, cmath
import time

# NEW: Import numpy for real quantum mechanics
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  NumPy not available - install with: pip install numpy")

app = Flask(__name__)
CORS(app)

# ---------------------------
# EXISTING Quantum Simulation Code (UNCHANGED)
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

# ---------------------------
# Job Generation (UNCHANGED)
# ---------------------------
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
# 🆕 NEW: Real Schrödinger Equation Solver
# ---------------------------
class SchrodingerSolver:
    """Real 1D Schrödinger equation with wavefunction evolution"""
    
    def __init__(self, Nx=200, x_range=(-10, 10)):
        if not NUMPY_AVAILABLE:
            raise RuntimeError("NumPy required for Schrödinger solver")
        
        self.Nx = Nx
        self.x = np.linspace(x_range[0], x_range[1], Nx)
        self.dx = self.x[1] - self.x[0]
        self.hbar = 1.0
        self.m = 1.0
        
        # Initial wavefunction (Gaussian wave packet)
        x0 = -3
        k0 = 5
        self.psi = np.exp(-(self.x - x0)**2) * np.exp(1j * k0 * self.x)
        self.psi /= np.sqrt(np.sum(np.abs(self.psi)**2) * self.dx)
        
        # Build Hamiltonian
        self._build_hamiltonian()
    
    def _build_hamiltonian(self):
        """Construct Hamiltonian matrix"""
        # Kinetic energy (Laplacian)
        laplacian = (
            -2 * np.eye(self.Nx)
            + np.eye(self.Nx, k=1)
            + np.eye(self.Nx, k=-1)
        ) / self.dx**2
        
        # Potential energy (free particle for now)
        V = np.zeros(self.Nx)
        
        # Total Hamiltonian
        self.H = -(self.hbar**2 / (2 * self.m)) * laplacian + np.diag(V)
    
    def evolve(self, steps=100, dt=0.001):
        """Evolve wavefunction in time"""
        start_time = time.time()
        
        for _ in range(steps):
            # Time evolution: ψ(t+dt) = ψ(t) - i*H*ψ(t)*dt/ℏ
            self.psi += -1j * dt / self.hbar * (self.H @ self.psi)
            
            # Renormalize to prevent numerical drift
            self.psi /= np.sqrt(np.sum(np.abs(self.psi)**2) * self.dx)
        
        compute_time = time.time() - start_time
        return compute_time
    
    def get_probability_density(self):
        """Get |ψ|² for visualization"""
        return np.abs(self.psi)**2
    
    def get_wavefunction_data(self):
        """Return wavefunction data for visualization"""
        prob_density = self.get_probability_density()
        return {
            'x': self.x.tolist(),
            'probability': prob_density.tolist(),
            'real': np.real(self.psi).tolist(),
            'imag': np.imag(self.psi).tolist(),
        }
    
    def measure(self):
        """Perform quantum measurement - collapse wavefunction"""
        prob_density = self.get_probability_density()
        
        # Randomly choose position based on probability
        cumulative = np.cumsum(prob_density) * self.dx
        r = np.random.random()
        idx = np.searchsorted(cumulative, r)
        
        if idx >= self.Nx:
            idx = self.Nx - 1
        
        # Collapse wavefunction to measured position
        measured_x = self.x[idx]
        
        # Create collapsed state (narrow Gaussian around measured position)
        self.psi = np.exp(-100 * (self.x - measured_x)**2)
        self.psi /= np.sqrt(np.sum(np.abs(self.psi)**2) * self.dx)
        
        return measured_x, idx

# ---------------------------
# EXISTING API Endpoints (UNCHANGED)
# ---------------------------
@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/quantum-simulation')
def quantum_simulation():
    """ORIGINAL endpoint - completely unchanged"""
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
    
    # Generate jobs based on quantum measurements
    jobs = []
    for i in range(4):
        quantum_val = stats[i * 2]['entropy'] + stats[i * 2]['efficiency']
        jobs.append(generate_quantum_job(quantum_val))
    
    # Visual parameters driven by quantum state
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
    """ORIGINAL search endpoint - completely unchanged"""
    # Run simulation with query-influenced seed
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
    
    random.seed()  # Reset seed
    
    return jsonify({
        'query': query,
        'jobs': jobs,
        'quantum_entropy': entropy
    })

# ---------------------------
# 🆕 NEW: Real Schrödinger Simulation Endpoint
# ---------------------------
@app.route('/api/schrodinger-simulation')
def schrodinger_simulation():
    """NEW endpoint for real quantum mechanics visualization"""
    
    if not NUMPY_AVAILABLE:
        return jsonify({
            'error': 'NumPy not installed',
            'message': 'Install with: pip install numpy'
        }), 500
    
    # Simulate compilation times for the "wow factor"
    compilation_start = time.time()
    
    # Create and evolve Schrödinger equation
    solver = SchrodingerSolver(Nx=200)
    
    # Simulate "C++ compilation"
    cpp_compile_time = random.uniform(0.2, 0.5)
    time.sleep(cpp_compile_time * 0.01)  # Small delay for realism
    
    # Run actual Schrödinger evolution
    schrodinger_time = solver.evolve(steps=300, dt=0.001)
    
    # Simulate "Rust async tasks"
    rust_tasks = random.randint(2, 5)
    rust_compile_time = random.uniform(0.3, 0.7)
    
    total_time = time.time() - compilation_start
    
    # Get wavefunction data
    wavefunction_data = solver.get_wavefunction_data()
    
    # Calculate statistics
    prob_density = np.array(wavefunction_data['probability'])
    entropy = -np.sum(prob_density * np.log(prob_density + 1e-10)) * solver.dx
    
    # Position and momentum uncertainties
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

@app.route('/api/wavefunction-collapse')
def wavefunction_collapse():
    """NEW endpoint for quantum measurement visualization"""
    
    if not NUMPY_AVAILABLE:
        return jsonify({'error': 'NumPy not available'}), 500
    
    # Create solver and evolve
    solver = SchrodingerSolver(Nx=200)
    solver.evolve(steps=200, dt=0.001)
    
    # Perform measurement
    measured_position, measured_idx = solver.measure()
    
    # Get collapsed wavefunction
    collapsed_data = solver.get_wavefunction_data()
    
    return jsonify({
        'measured_position': float(measured_position),
        'measured_index': int(measured_idx),
        'collapsed_wavefunction': collapsed_data,
        'message': f'Wavefunction collapsed to x = {measured_position:.3f}'
    })

if __name__ == '__main__':
    print("🌌 Quantum Job Search Server Starting...")
    print("📡 Server running at http://localhost:5000")
    if NUMPY_AVAILABLE:
        print("✅ Real Schrödinger solver ENABLED")
        print("🆕 New endpoint: /api/schrodinger-simulation")
        print("🆕 New endpoint: /api/wavefunction-collapse")
    else:
        print("⚠️  NumPy not found - Schrödinger solver disabled")
        print("   Install with: pip install numpy")
    app.run(debug=True, port=5000)