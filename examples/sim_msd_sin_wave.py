import numpy as np
from math_utils import StateVec, StateDerivativeVec, getMagnitude, getUnitVector
from point_masses_simulation import PointMassesSimulation


def main():
    k_s = 1000
    k_d = 0.75
    m = 0.010
    n_m = 14
    n_nodes = n_m + 2
    l_cord = 1
    l_cord_step = l_cord/(n_m+1)
    g = 0 #9.81
    dt = 0.002
    sim_time = 10.0
    # f_external = np.array([0, 50])

    # drive parameters
    amp = 0.15 # amplitude ()
    c = l_cord_step * np.sqrt(k_s/m)
    # omega = np.pi * c / l_cord
    freq = 6.5 # Hz
    omega = 2*np.pi*freq
    one_oscillation_time = 2*np.pi/omega*2

    def f(t, x: StateVec, f_external_applied: bool):
        x_dot = StateDerivativeVec(n_nodes)

        if t <= one_oscillation_time:
        # drive BC at left end
            yL = amp * np.sin(omega * t)
            vL = amp * omega * np.cos(omega * t)
            aL = -amp * (omega**2) * np.sin(omega * t)

            # kinematics at left end
            x.p_y[0] = yL
            x.v_y[0] = vL
            x.p_x[0] = 0.0
            x.v_x[0] = 0.0

            # derivatives for boundary nodes
            x_dot.v_x[0] = 0.0
            x_dot.v_y[0] = vL          # dp_y/dt = vL
            x_dot.a_x[0] = 0.0
            x_dot.a_y[0] = aL          # dv_y/dt = aL

        else:
            # kinematics at left end
            x.p_y[0] = 0
            x.v_y[0] = 0
            x.p_x[0] = 0
            x.v_x[0] = 0

            # derivatives for boundary nodes
            x_dot.v_x[0] = 0
            x_dot.v_y[0] = 0          # dp_y/dt = vL
            x_dot.a_x[0] = 0
            x_dot.a_y[0] = 0          # dv_y/dt = aL

        # kinematics at right end
        x.p_x[-1] = l_cord
        x.p_y[-1] = 0.0
        x.v_x[-1] = 0.0
        x.v_y[-1] = 0.0


        # kinematics at every node
        x_dot.v_x[:] = x.v_x
        x_dot.v_y[:] = x.v_y

        for i in range(0, n_nodes):
            if i == 0:
                dist_next = getMagnitude(x.p(i), x.p(i+1))
                unit_next = getUnitVector(x.p(i), x.p(i+1))
                f_s_next = -k_s * (dist_next - l_cord_step) * unit_next
                f_d_next = -k_d * (x.v(i) - x.v(i+1))
                # f_total = f_s_next + f_d_next np.sin()
                if f_external_applied:
                    f_total = f_s_next + f_d_next #+ f_external
                else:
                    f_total = f_s_next + f_d_next
            elif i == (n_nodes-1):
                dist_prev = getMagnitude(x.p(i), x.p(i-1))
                unit_prev = getUnitVector(x.p(i), x.p(i-1))
                f_s_prev = k_s * (dist_next - l_cord_step) * unit_next
                f_d_prev = k_d * (x.v(i) - x.v(i-1))
                f_total = f_s_prev + f_d_prev
            else:
                dist_prev = getMagnitude(x.p(i), x.p(i-1))
                unit_prev = getUnitVector(x.p(i), x.p(i-1))
                f_s_previous = -k_s * (dist_prev - l_cord_step) * unit_prev
                
                dist_next = getMagnitude(x.p(i), x.p(i+1))
                unit_next = getUnitVector(x.p(i+1), x.p(i))
                f_s_next = k_s * (dist_next - l_cord_step) * unit_next
                
                f_d_previous = -k_d * (x.v(i) - x.v(i-1))
                f_d_next = -k_d * (x.v(i) - x.v(i+1))

                if f_external_applied:
                    f_total = f_s_previous + f_s_next + f_d_previous + f_d_next #+ f_external
                else:
                    f_total = f_s_previous + f_s_next + f_d_previous + f_d_next
            
            a_i = f_total / m - np.array([0, g])
            
            x_dot.a_x[i] = a_i[0]
            x_dot.a_y[i] = a_i[1]
        
        # x_dot.v_x[0] = x_dot.v_y[0] = x_dot.a_x[0] = x_dot.a_y[0] = 0
        # x_dot.v_x[-1] = x_dot.v_y[-1] = x_dot.a_x[-1] = x_dot.a_y[-1] = 0

        # derivatives for boundary nodes 
        # left node derivative = prescribed trajectory derivatives
        # x_dot.v_x[0] = 0.0
        # x_dot.v_y[0] = vL          # dp_y/dt = vL
        # x_dot.a_x[0] = 0.0
        # x_dot.a_y[0] = aL          # dv_y/dt = aL

        # right node remains clamped
        x_dot.v_x[-1] = x_dot.v_y[-1] = 0.0
        x_dot.a_x[-1] = x_dot.a_y[-1] = 0.0

        return x_dot
        
    sim = PointMassesSimulation(f=f, k_s=k_s, k_d=k_d, m=m, n_m=n_m, 
                                l_cord=l_cord, g=g, dt=dt, sim_time=sim_time)
    
    sim.sim()

if __name__ == "__main__":
    main()