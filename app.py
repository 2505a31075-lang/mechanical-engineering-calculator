from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

G = 9.81  # gravité standard

# ============================================================
#  1. MECHANICS
# ============================================================

def calc_force(m, a):
    return m * a

def calc_work(F, d, theta):
    return F * d * math.cos(math.radians(theta))

def calc_power_mech(W, t):
    return W / t

def calc_kinetic_energy(m, v):
    return 0.5 * m * v ** 2

# ============================================================
#  2. STRENGTH OF MATERIALS
# ============================================================

def calc_stress(F, A):
    return F / A

def calc_strain(dL, L):
    return dL / L

def calc_young_modulus(sigma, epsilon):
    return sigma / epsilon

# ============================================================
#  3. THERMODYNAMICS
# ============================================================

def calc_heat_transfer(m, c, dT):
    return m * c * dT

def calc_thermo_work(P, dV):
    return P * dV

def calc_thermal_efficiency(W_net, Q_in):
    return W_net / Q_in

# ============================================================
#  4. FLUID MECHANICS
# ============================================================

def calc_pressure(rho, h):
    return rho * G * h

def calc_reynolds(rho, v, D, mu):
    return (rho * v * D) / mu

def calc_flow_velocity(Q, A):
    return Q / A

def calc_discharge(A, v):
    return A * v

# ============================================================
#  5. THERMAL ENGINEERING
# ============================================================

def calc_heat_conduction(k, A, dT, L):
    return (k * A * dT) / L

def calc_cop(Q, W):
    return Q / W

def calc_heat_engine_eff(Qh, Qc):
    return 1 - (Qc / Qh)

# ============================================================
#  6. MACHINE DESIGN
# ============================================================

def calc_torque(F, r):
    return F * r

def calc_shaft_power(N, T):
    return (2 * math.pi * N * T) / 60

def calc_shaft_diameter(T, tau):
    return ((16 * T) / (math.pi * tau)) ** (1 / 3)

# ============================================================
#  ROUTES
# ============================================================

@app.route('/')
def home():
    return render_template('base.html')

# ------- MECHANICS -------
@app.route('/mechanics', methods=['GET', 'POST'])
def mechanics():
    results = {}
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        try:
            if action == 'force':
                m = float(data['mass'])
                a = float(data['acceleration'])
                result = calc_force(m, a)
                results = {'force': f"{result:.4f} N"}
            
            elif action == 'work':
                F = float(data['force'])
                d = float(data['distance'])
                theta = float(data['angle'])
                result = calc_work(F, d, theta)
                results = {'work': f"{result:.4f} J"}
            
            elif action == 'power':
                W = float(data['work'])
                t = float(data['time'])
                result = calc_power_mech(W, t)
                results = {'power': f"{result:.4f} W"}
            
            elif action == 'kinetic':
                m = float(data['mass'])
                v = float(data['velocity'])
                result = calc_kinetic_energy(m, v)
                results = {'kinetic_energy': f"{result:.4f} J"}
            
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('mechanics.html')

# ------- STRENGTH OF MATERIALS -------
@app.route('/strength', methods=['GET', 'POST'])
def strength():
    results = {}
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        try:
            if action == 'stress':
                F = float(data['force'])
                A = float(data['area'])
                result = calc_stress(F, A)
                results = {
                    'stress_pa': f"{result:.4f} Pa",
                    'stress_mpa': f"{result / 1e6:.4f} MPa"
                }
            
            elif action == 'strain':
                dL = float(data['delta_length'])
                L = float(data['length'])
                result = calc_strain(dL, L)
                results = {'strain': f"{result:.6f}"}
            
            elif action == 'young':
                sigma = float(data['stress'])
                epsilon = float(data['strain'])
                result = calc_young_modulus(sigma, epsilon)
                results = {
                    'young_pa': f"{result:.4e} Pa",
                    'young_gpa': f"{result / 1e9:.4f} GPa"
                }
            
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('strength.html')

# ------- THERMODYNAMICS -------
@app.route('/thermodynamics', methods=['GET', 'POST'])
def thermodynamics():
    results = {}
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        try:
            if action == 'heat':
                m = float(data['mass'])
                c = float(data['specific_heat'])
                dT = float(data['delta_temp'])
                result = calc_heat_transfer(m, c, dT)
                results = {'heat': f"{result:.4f} J"}
            
            elif action == 'work':
                P = float(data['pressure'])
                dV = float(data['delta_volume'])
                result = calc_thermo_work(P, dV)
                results = {'work': f"{result:.4f} J"}
            
            elif action == 'efficiency':
                W_net = float(data['net_work'])
                Q_in = float(data['heat_in'])
                result = calc_thermal_efficiency(W_net, Q_in)
                results = {
                    'efficiency': f"{result:.4f}",
                    'efficiency_percent': f"{result * 100:.2f}%"
                }
            
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('thermodynamics.html')

# ------- FLUID MECHANICS -------
@app.route('/fluid', methods=['GET', 'POST'])
def fluid():
    results = {}
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        try:
            if action == 'pressure':
                rho = float(data['density'])
                h = float(data['height'])
                result = calc_pressure(rho, h)
                results = {
                    'pressure_pa': f"{result:.4f} Pa",
                    'pressure_kpa': f"{result / 1000:.4f} kPa"
                }
            
            elif action == 'reynolds':
                rho = float(data['density'])
                v = float(data['velocity'])
                D = float(data['diameter'])
                mu = float(data['viscosity'])
                result = calc_reynolds(rho, v, D, mu)
                regime = "LAMINAR" if result < 2300 else ("TURBULENT" if result > 4000 else "TRANSITIONAL")
                results = {
                    'reynolds': f"{result:.2f}",
                    'regime': regime
                }
            
            elif action == 'velocity':
                Q = float(data['flow_rate'])
                A = float(data['area'])
                result = calc_flow_velocity(Q, A)
                results = {'velocity': f"{result:.4f} m/s"}
            
            elif action == 'discharge':
                A = float(data['area'])
                v = float(data['velocity'])
                result = calc_discharge(A, v)
                results = {
                    'discharge_m3s': f"{result:.4f} m³/s",
                    'discharge_ls': f"{result * 1000:.4f} L/s"
                }
            
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('fluid.html')

# ------- THERMAL ENGINEERING -------
@app.route('/thermal_eng', methods=['GET', 'POST'])
def thermal_eng():
    results = {}
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        try:
            if action == 'conduction':
                k = float(data['conductivity'])
                A = float(data['area'])
                dT = float(data['delta_temp'])
                L = float(data['thickness'])
                result = calc_heat_conduction(k, A, dT, L)
                results = {'conduction': f"{result:.4f} W"}
            
            elif action == 'cop':
                Q = float(data['heat'])
                W = float(data['work'])
                kind = data.get('type', 'Refrigerator')
                result = calc_cop(Q, W)
                results = {'cop': f"{kind} COP = {result:.4f}"}
            
            elif action == 'engine_eff':
                Qh = float(data['heat_hot'])
                Qc = float(data['heat_cold'])
                result = calc_heat_engine_eff(Qh, Qc)
                results = {
                    'efficiency': f"{result:.4f}",
                    'efficiency_percent': f"{result * 100:.2f}%"
                }
            
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('thermal_eng.html')

# ------- MACHINE DESIGN -------
@app.route('/machine_design', methods=['GET', 'POST'])
def machine_design():
    results = {}
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        try:
            if action == 'torque':
                F = float(data['force'])
                r = float(data['radius'])
                result = calc_torque(F, r)
                results = {'torque': f"{result:.4f} N.m"}
            
            elif action == 'power':
                N = float(data['speed'])
                T = float(data['torque'])
                result = calc_shaft_power(N, T)
                results = {
                    'power_w': f"{result:.4f} W",
                    'power_kw': f"{result / 1000:.4f} kW"
                }
            
            elif action == 'diameter':
                T = float(data['torque'])
                tau = float(data['shear_stress'])
                result = calc_shaft_diameter(T, tau)
                results = {
                    'diameter_m': f"{result:.6f} m",
                    'diameter_mm': f"{result * 1000:.3f} mm"
                }
            
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('machine_design.html')

# ============================================================
#  ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
