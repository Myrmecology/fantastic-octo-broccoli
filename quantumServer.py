"""
Quantum Job Search Server
Connects quantum simulation to WebGL frontend
"""

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import math, random, cmath

app = Flask(__name__)
CORS(app)

# ---------------------------
# Quantum Simulation Code
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
# Job Generation
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
# API Endpoints
# ---------------------------
@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/quantum-simulation')
def quantum_simulation():
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

if __name__ == '__main__':
    print("🌌 Quantum Job Search Server Starting...")
    print("📡 Server running at http://localhost:5000")
    app.run(debug=True, port=5000)