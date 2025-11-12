import numpy as np
import matplotlib.pyplot as plt
from point_masses_simulation import PointMassesSimulation
from math_utils import StateVec, StateDerivativeVec, getMagnitude, getUnitVector

def run_comparison():
    """
    Compare MSD simulation with wave equation solution
    Tune parameters to get matching behavior
    """
    
    # MSD Parameters
    k_s = 1000    # Spring constant
    k_d = 1.0     # Damping constant
    m = 0.010     # Mass per point
    n_m = 14      # Number of masses
    n_nodes = n_m + 2
    l_cord = 1    # Total cord length
    l_cord_step = l_cord/(n_m+1)
    g = 9.81
    dt = 0.002
    
    # Calculate theoretical wave speed for comparison
    # For a string: c = sqrt(T/μ) where T is tension, μ is linear density
    mu = m * n_m / l_cord  # Linear mass density
    
    # Estimate tension from spring system
    # At equilibrium with gravity: T ≈ k_s * stretch
    # This is approximate - you'll need to tune
    estimated_stretch = (m * g * n_m) / (2 * k_s)  # Very rough estimate
    T_estimate = k_s * estimated_stretch
    c_estimate = np.sqrt(T_estimate / mu)
    
    print(f"System Parameters:")
    print(f"  Spring constant k_s = {k_s} N/m")
    print(f"  Damping constant k_d = {k_d} N·s/m")
    print(f"  Mass per point m = {m} kg")
    print(f"  Number of masses = {n_m}")
    print(f"  Cord length = {l_cord} m")
    print(f"\nEstimated wave parameters:")
    print(f"  Linear density μ = {mu:.4f} kg/m")
    print(f"  Estimated tension T ≈ {T_estimate:.2f} N")
    print(f"  Estimated wave speed c ≈ {c_estimate:.2f} m/s")
    print(f"\nFor wave equation, try c values between {0.5*c_estimate:.1f} and {2*c_estimate:.1f} m/s")
    
    # Theoretical damping time scale
    tau_damping = m / k_d
    print(f"  Damping time scale τ = m/k_d = {tau_damping:.3f} s")
    
    # Calculate natural frequencies
    # For fixed-fixed string: f_n = n*c/(2L) for n = 1,2,3,...
    for n in range(1, 4):
        f_n = n * c_estimate / (2 * l_cord)
        print(f"  Mode {n} frequency: f_{n} ≈ {f_n:.2f} Hz")


def compare_equilibrium_shapes():
    """
    Compare the equilibrium hanging shape between MSD and analytical solution
    """
    # MSD Parameters
    k_s = 1000
    k_d = 10.0  # Higher damping to reach equilibrium faster
    m = 0.010
    n_m = 14
    n_nodes = n_m + 2
    l_cord = 1
    l_cord_step = l_cord/(n_m+1)
    g = 9.81
    dt = 0.001
    
    # Run MSD until equilibrium
    print("Running MSD to equilibrium...")
    
    def f(t, x: StateVec):
        x_dot = StateDerivativeVec(n_nodes)
        x_dot.v_x[:] = x.v_x
        x_dot.v_y[:] = x.v_y

        for i in range(1, n_m+1):
            dist_prev = getMagnitude(x.p(i), x.p(i-1))
            unit_prev = getUnitVector(x.p(i), x.p(i-1))
            f_s_previous = -k_s * (dist_prev - l_cord_step) * unit_prev
            
            dist_next = getMagnitude(x.p(i), x.p(i+1))
            unit_next = getUnitVector(x.p(i+1), x.p(i))
            f_s_next = k_s * (dist_next - l_cord_step) * unit_next
            
            f_d_previous = -k_d * (x.v(i) - x.v(i-1))
            f_d_next = -k_d * (x.v(i) - x.v(i+1))

            f_total = f_s_previous + f_s_next + f_d_previous + f_d_next
            a_i = f_total / m - np.array([0, g])
            
            x_dot.a_x[i] = a_i[0]
            x_dot.a_y[i] = a_i[1]
        
        x_dot.v_x[0] = x_dot.v_y[0] = x_dot.a_x[0] = x_dot.a_y[0] = 0
        x_dot.v_x[-1] = x_dot.v_y[-1] = x_dot.a_x[-1] = x_dot.a_y[-1] = 0

        return x_dot
    
    # Create system and run to equilibrium
    from point_masses_system import PointMassesSystem
    system = PointMassesSystem(f=f, k_s=k_s, k_d=k_d, m=m, n_m=n_m, 
                               l_cord=l_cord, g=g, dt=dt)
    
    # Run for a while to reach equilibrium
    equilibrium_time = 5.0
    n_steps = int(equilibrium_time / dt)
    
    for _ in range(n_steps):
        system.step()
    
    # Extract equilibrium shape
    x_eq = np.array(system.x.p_x)
    y_eq = np.array(system.x.p_y)
    
    # Analytical solution for hanging chain (catenary)
    # For small sag, approximately parabolic: y(x) = -a*x*(L-x)
    # where a depends on weight and tension
    
    # Plot comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot shapes
    ax1.plot(x_eq, y_eq, 'ro-', label='MSD Equilibrium', markersize=6)
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.set_title('Equilibrium Shape Comparison')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_aspect('equal')
    
    # Plot sag profile
    ax2.plot(x_eq[1:-1], y_eq[1:-1], 'ro', label='MSD Points')
    
    # Fit parabola to MSD data
    coeffs = np.polyfit(x_eq[1:-1], y_eq[1:-1], 2)
    x_fit = np.linspace(x_eq[1], x_eq[-2], 100)
    y_fit = np.polyval(coeffs, x_fit)
    ax2.plot(x_fit, y_fit, 'b-', label=f'Parabolic Fit', alpha=0.7)
    
    ax2.set_xlabel('x (m)')
    ax2.set_ylabel('y (m)')
    ax2.set_title('Sag Profile')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
    
    print(f"\nEquilibrium shape achieved:")
    print(f"  Maximum sag: {abs(min(y_eq)):.4f} m")
    print(f"  Parabolic fit coefficients: a={coeffs[0]:.4f}, b={coeffs[1]:.4f}, c={coeffs[2]:.4f}")
    
    return x_eq, y_eq


if __name__ == "__main__":
    print("=" * 60)
    print("PARAMETER ESTIMATION FOR WAVE EQUATION")
    print("=" * 60)
    run_comparison()
    
    print("\n" + "=" * 60)
    print("EQUILIBRIUM SHAPE ANALYSIS")
    print("=" * 60)
    x_eq, y_eq = compare_equilibrium_shapes()