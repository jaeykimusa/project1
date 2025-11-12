# sim_fixed_ends_wave.py
import numpy as np
from math_utils import StateVec, StateDerivativeVec, getMagnitude, getUnitVector
from point_masses_simulation import PointMassesSimulation

def main():
    # --------- Physical / discretization parameters ----------
    L = 1.0              # total length (m)
    n_total = 14         # TOTAL nodes including the two fixed endpoints
    n_m = n_total - 2    # interior (moving) masses
    n_nodes = n_m + 2
    dx = L / (n_nodes - 1)

    # Choose a light, “clean” set (works well and matches our earlier mapping)
    m  = 0.020           # kg per node
    k_s = 800.0          # N/m
    k_d = 3.2            # N·s/m
    g  = 0.0             # no gravity for clean fixed–end wave comparison

    # Time settings
    dt = 0.005            # stable and accurate
    sim_time = 10.0       # seconds

    # --------- RHS (forces) exactly like your style ----------
    def f(t, x: StateVec):
        x_dot = StateDerivativeVec(n_nodes)

        # kinematics
        x_dot.v_x[:] = x.v_x
        x_dot.v_y[:] = x.v_y

        # dynamics (interior nodes 1..n_m)
        for i in range(1, n_m + 1):
            # left neighbor
            dist_L = getMagnitude(x.p(i), x.p(i-1))
            dir_L  = getUnitVector(x.p(i), x.p(i-1))     # (pi - p_{i-1})/||...||
            F_s_L  = -k_s * (dist_L - dx) * dir_L
            F_d_L  = -k_d * (x.v(i) - x.v(i-1))

            # right neighbor
            dist_R = getMagnitude(x.p(i), x.p(i+1))
            # note the direction choice mirrors your example file
            dir_R  = getUnitVector(x.p(i+1), x.p(i))     # (p_{i+1} - pi)/||...||
            F_s_R  =  k_s * (dist_R - dx) * dir_R
            F_d_R  = -k_d * (x.v(i) - x.v(i+1))

            F_tot = F_s_L + F_s_R + F_d_L + F_d_R + np.array([0.0, -m*g])
            a_i   = F_tot / m
            x_dot.a_x[i] = a_i[0]
            x_dot.a_y[i] = a_i[1]

        # clamp endpoints (fixed supports)
        x_dot.v_x[0] = x_dot.v_y[0] = x_dot.a_x[0] = x_dot.a_y[0] = 0.0
        x_dot.v_x[-1] = x_dot.v_y[-1] = x_dot.a_x[-1] = x_dot.a_y[-1] = 0.0

        return x_dot

    # --------- Build the simulation object ----------
    sim = PointMassesSimulation(
        f=f, k_s=k_s, k_d=k_d, m=m, n_m=n_m, l_cord=L, g=g, dt=dt, sim_time=sim_time
    )

    # --------- Initial condition = pure first mode (sine) ----------
    # This gives a clean “sin wave” oscillation between fixed ends.
    H = 0.01  # amplitude (m)
    for i in range(n_nodes):
        x_i = i * dx
        sim.system.x.p_y[i] = H * np.sin(np.pi * x_i / L)   # u(x,0) = H*sin(pi x / L)
        sim.system.x.v_x[i] = 0.0
        sim.system.x.v_y[i] = 0.0

    # endpoints stay zero from the sine anyway, but we explicitly enforce:
    sim.system.x.p_y[0]  = 0.0
    sim.system.x.p_y[-1] = 0.0

    # --------- Run the animation with your existing styling ----------
    sim.sim()

if __name__ == "__main__":
    main()
