import numpy as np
from math_utils import StateVec, StateDerivativeVec, getMagnitude, getUnitVector
from point_masses_simulation import PointMassesSimulation


def main():
    k_s = 1000
    k_d = 1.1
    m = 0.010
    n_m = 50
    n_nodes = n_m + 2
    l_cord = 1
    l_cord_step = l_cord/(n_m+1)
    g = 9.81
    dt = 0.002
    sim_time = 10.0
    f_external = np.array([0, 50])

    def f(t, x: StateVec, f_external_applied: bool):
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

            if f_external_applied:
                f_total = f_s_previous + f_s_next + f_d_previous + f_d_next + f_external
            else:
                f_total = f_s_previous + f_s_next + f_d_previous + f_d_next
            
            a_i = f_total / m - np.array([0, g])
            
            x_dot.a_x[i] = a_i[0]
            x_dot.a_y[i] = a_i[1]
        
        x_dot.v_x[0] = x_dot.v_y[0] = x_dot.a_x[0] = x_dot.a_y[0] = 0
        x_dot.v_x[-1] = x_dot.v_y[-1] = x_dot.a_x[-1] = x_dot.a_y[-1] = 0

        return x_dot
        
    sim = PointMassesSimulation(f=f, k_s=k_s, k_d=k_d, m=m, n_m=n_m, 
                                l_cord=l_cord, g=g, dt=dt, sim_time=sim_time)
    
    sim.sim()

if __name__ == "__main__":
    main()