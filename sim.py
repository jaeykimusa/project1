ççimport math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from math_utils import StateVec, StateDerivativeVec, getMagnitude, getUnitVector
from rk4 import RK4

class PointMassesSystem:
    def __init__(
                this, 
                f: callable,
                k_s: float,
                k_d: float,
                m: float,
                n_m: float,
                l_cord: float,
                g: float,
                dt: float):

        # define the system values
        this.k_s = k_s
        this.k_d = k_d
        this.m = m

        this.n_m = n_m
        this.n_nodes = n_m + 2
        this.l_cord = l_cord

        this.g = g

        x = StateVec(this.n_nodes)
        l_cord_step = this.l_cord / (this.n_m+1)
        for i in range(n_m+1):
            x.p_x[i+1] = (i+1) * l_cord_step
        this.x = x

        # initial perturbation
        for i in range(1, n_m+1):
            x.p_y[i] = 0.05 * np.sin(np.pi * x.p_x[i] / this.l_cord)

        this.rk4 = RK4(function=f, y_0=this.x, x_0=0, h=dt)

    def step(this):
        this.x = this.rk4.step()
        # this.x.print()
        return this.x
    
    # def getState(this):
    #     return this.x
    
        



class PointMassesSimulation:
    def __init__(
                this, 
                f: callable,
                k_s: float,
                k_d: float,
                m: float,
                n_m: float,
                l_cord: float,
                g: float,
                dt: float,
                sim_time: float):
        
        # define the system and initialize the state
        this.system = PointMassesSystem(f=f, k_s=k_s, k_d=k_d, m=m, n_m=n_m, l_cord=l_cord, g=g, dt=dt)

        # define time values
        this.time = 0
        this.sim_time = sim_time
        this.dt = dt

        # add initial data
        this.data = [this.time, this.system.x]


    def create(this):
        pass

    def step(this):
        # x = this.system.step()
        this.time += this.dt
        this.data.append([this.time, this.system.step()])

    def sync(this):
        pass

    def sim(this):
        while(this.time <= this.sim_time):
            this.step()
            this.system.x.print()

    def plot(this):
        pass

    def animate(self, filename='bungee_simulation.mp4', fps=30, skip_frames=1):
        """
        Create an animation of the simulation.
        
        Parameters:
            filename: Output video filename
            fps: Frames per second
            skip_frames: Show every Nth frame (1 = show all frames)
        """
        # Extract data
        times = [d[0] for d in self.data]
        states = [d[1] for d in self.data]
        
        # Get bounds for plotting
        all_x = [state.p_x for state in states]
        all_y = [state.p_y for state in states]
        
        x_min = min([x.min() for x in all_x]) - 0.1
        x_max = max([x.max() for x in all_x]) + 0.1
        y_min = min([y.min() for y in all_y]) - 0.2
        y_max = max([y.max() for y in all_y]) + 0.2
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xlabel('x (m)', fontsize=12)
        ax.set_ylabel('y (m)', fontsize=12)
        ax.set_title('Bungee Cord Simulation', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.set_aspect('equal')
        
        # Initialize line and points
        line, = ax.plot([], [], 'b-', linewidth=2.5, label='Cord')
        masses, = ax.plot([], [], 'ko', markersize=8, label='Masses')
        endpoints, = ax.plot([], [], 'ro', markersize=12, label='Fixed Ends', zorder=10)
        
        # Time text
        time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                           fontsize=11, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Energy text (optional)
        energy_text = ax.text(0.02, 0.88, '', transform=ax.transAxes,
                             fontsize=10, verticalalignment='top',
                             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        ax.legend(loc='upper right', fontsize=10)
        
        def init():
            line.set_data([], [])
            masses.set_data([], [])
            endpoints.set_data([], [])
            time_text.set_text('')
            energy_text.set_text('')
            return line, masses, endpoints, time_text, energy_text
        
        def animate_frame(frame_idx):
            idx = frame_idx * skip_frames
            if idx >= len(states):
                idx = len(states) - 1
            
            state = states[idx]
            t = times[idx]
            
            # Get positions
            x_pos = state.p_x
            y_pos = state.p_y
            
            # Update line (cord)
            line.set_data(x_pos, y_pos)
            
            # Update interior masses (excluding endpoints)
            masses.set_data(x_pos[1:-1], y_pos[1:-1])
            
            # Update fixed endpoints
            endpoints.set_data([x_pos[0], x_pos[-1]], [y_pos[0], y_pos[-1]])
            
            # Update time
            time_text.set_text(f'Time: {t:.3f} s\nStep: {idx}')
            
            # Calculate and display energy (optional)
            energy = self._calculate_energy(state)
            energy_text.set_text(f'Energy: {energy:.4f} J')
            
            return line, masses, endpoints, time_text, energy_text
        
        # Create animation
        n_frames = len(states) // skip_frames
        anim = animation.FuncAnimation(fig, animate_frame, init_func=init,
                                      frames=n_frames, interval=1000/fps,
                                      blit=True, repeat=True)
        
        # Save animation
        print(f"Saving animation to {filename}...")
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, bitrate=2400)
        anim.save(filename, writer=writer)
        plt.close()
        
        print(f"✓ Animation saved successfully!")
    
    def _calculate_energy(self, state):
        """Calculate total mechanical energy of the system."""
        KE = 0  # Kinetic energy
        PE = 0  # Potential energy (spring + gravity)
        
        # Kinetic energy
        for i in range(1, self.system.n_nodes - 1):  # Exclude fixed endpoints
            v = state.v(i)
            KE += 0.5 * self.system.m * np.dot(v, v)
        
        # Spring potential energy
        for i in range(self.system.n_nodes - 1):
            p_i = state.p(i)
            p_next = state.p(i + 1)
            dist = getMagnitude(p_i, p_next)
            l_rest = self.system.l_cord / (self.system.n_m + 1)
            PE += 0.5 * self.system.k_s * (dist - l_rest)**2
        
        # Gravitational potential energy
        for i in range(1, self.system.n_nodes - 1):
            PE += self.system.m * self.system.g * state.p_y[i]
        
        return KE + PE


# def main():
#     k_s = 1000
#     k_d = 1.0
#     m = 0.010
#     n_m = 14
#     n_nodes = n_m + 2
#     l_cord = 1
#     l_cord_step = l_cord/(n_m+1)
#     g = 9.81
#     dt = 0.01
#     sim_time = 60

#     # function f(t,x)
#     def f(t, x: StateVec):
#         x_dot = StateDerivativeVec(n_nodes)
#         x_dot.v_x = x.v_x
#         x_dot.v_y = x.v_y

#         for i in range(1,n_m+1):
#             f_s_previous = -k_s * (getMagnitude(x.p(i), x.p(i-1))-l_cord_step) * getUnitVector(x.p(i), x.p(i-1))
#             f_s_next = -k_s * (getMagnitude(x.p(i), x.p(i+1))-l_cord_step) * getUnitVector(x.p(i), x.p(i+1))
#             f_d_previous = -k_d * (x.v(i)-x.v(i-1))
#             f_d_next = -k_d * (x.v(i)-x.v(i+1))

#             a_i = (f_s_previous+f_s_next+f_d_previous+f_d_next)/m - np.array([0,g])
#             x_dot.a_x[i] = a_i[0]
#             x_dot.a_y[i] = a_i[1]

#         return x_dot
        
#     sim = PointMassesSimulation(f=f, k_s=k_s, k_d=k_d, m=m, n_m=n_m, l_cord=l_cord, g=g, dt=dt, sim_time=sim_time)
#     sim.sim()

def main():
    k_s = 1000
    k_d = 1.0
    m = 0.010
    n_m = 14
    n_nodes = n_m + 2
    l_cord = 1
    l_cord_step = l_cord/(n_m+1)
    g = 9.81
    dt = 0.001  # Smaller time step for stability
    sim_time = 5.0  # Start with shorter simulation

    # function f(t,x)
    def f(t, x: StateVec):
        x_dot = StateDerivativeVec(n_nodes)
        x_dot.v_x[:] = x.v_x
        x_dot.v_y[:] = x.v_y

        for i in range(1, n_m+1):
            # Spring force from left
            dist_prev = getMagnitude(x.p(i), x.p(i-1))
            unit_prev = getUnitVector(x.p(i), x.p(i-1))
            f_s_previous = -k_s * (dist_prev - l_cord_step) * unit_prev
            
            # Spring force from right
            dist_next = getMagnitude(x.p(i), x.p(i+1))
            unit_next = getUnitVector(x.p(i+1), x.p(i))
            f_s_next = k_s * (dist_next - l_cord_step) * unit_next
            
            # Damper forces
            f_d_previous = -k_d * (x.v(i) - x.v(i-1))
            f_d_next = -k_d * (x.v(i) - x.v(i+1))

            # Total acceleration
            f_total = f_s_previous + f_s_next + f_d_previous + f_d_next
            a_i = f_total / m - np.array([0, g])
            
            # ✅ Assign to specific indices
            x_dot.a_x[i] = a_i[0]
            x_dot.a_y[i] = a_i[1]
        
        # Fix boundaries
        x_dot.v_x[0] = x_dot.v_y[0] = x_dot.a_x[0] = x_dot.a_y[0] = 0
        x_dot.v_x[-1] = x_dot.v_y[-1] = x_dot.a_x[-1] = x_dot.a_y[-1] = 0

        return x_dot
        
    sim = PointMassesSimulation(f=f, k_s=k_s, k_d=k_d, m=m, n_m=n_m, 
                                l_cord=l_cord, g=g, dt=dt, sim_time=sim_time)
    
    # Add initial displacement (sine wave)
    for i in range(1, n_m+1):
        sim.system.x.p_y[i] = 0.05 * np.sin(np.pi * sim.system.x.p_x[i] / l_cord)
    
    print("Initial state:")
    sim.system.x.print()
    
    sim.sim()
    sim.animate()


if __name__ == "__main__":
    main()