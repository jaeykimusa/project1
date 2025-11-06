import math
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
        for i in range(this.n_nodes):
            x.p_x[i] = i * l_cord_step
        this.x = x

        this.rk4 = RK4(function=f, y_0=this.x, x_0=0, h=dt)

    def step(this):
        this.x = this.rk4.step()
        return this.x


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
        this.data = [[this.time, this.system.x]]

    def step(this):
        this.time += this.dt
        this.data.append([this.time, this.system.step()])

    def sim(this):
        while(this.time <= this.sim_time):
            this.step()
            if len(this.data) % 100 == 0:
                print(f"Progress: {this.time:.2f}/{this.sim_time:.2f} s")

    def animate(this, filename='bungee_simulation.mp4', fps=30, skip_frames=1):
        """Create animation of the simulation."""
        times = [d[0] for d in this.data]
        states = [d[1] for d in this.data]
        
        all_x = [state.p_x for state in states]
        all_y = [state.p_y for state in states]
        
        x_min = min([x.min() for x in all_x]) - 0.1
        x_max = max([x.max() for x in all_x]) + 0.1
        y_min = min([y.min() for y in all_y]) - 0.2
        y_max = max([y.max() for y in all_y]) + 0.2
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xlabel('x (m)', fontsize=12)
        ax.set_ylabel('y (m)', fontsize=12)
        ax.set_title('Bungee Cord Simulation', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.set_aspect('equal')
        
        line, = ax.plot([], [], 'b-', linewidth=2.5, label='Cord')
        masses, = ax.plot([], [], 'ko', markersize=8, label='Masses')
        endpoints, = ax.plot([], [], 'ro', markersize=12, label='Fixed Ends', zorder=10)
        
        time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                           fontsize=11, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.legend(loc='upper right', fontsize=10)
        
        def init():
            line.set_data([], [])
            masses.set_data([], [])
            endpoints.set_data([], [])
            time_text.set_text('')
            return line, masses, endpoints, time_text
        
        def animate_frame(frame_idx):
            idx = frame_idx * skip_frames
            if idx >= len(states):
                idx = len(states) - 1
            
            state = states[idx]
            t = times[idx]
            
            x_pos = state.p_x
            y_pos = state.p_y
            
            line.set_data(x_pos, y_pos)
            masses.set_data(x_pos[1:-1], y_pos[1:-1])
            endpoints.set_data([x_pos[0], x_pos[-1]], [y_pos[0], y_pos[-1]])
            time_text.set_text(f'Time: {t:.3f} s\nStep: {idx}')
            
            return line, masses, endpoints, time_text
        
        n_frames = len(states) // skip_frames
        anim = animation.FuncAnimation(fig, animate_frame, init_func=init,
                                      frames=n_frames, interval=1000/fps,
                                      blit=True, repeat=True)
        
        print(f"Saving animation to {filename}...")
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, bitrate=2400)
        anim.save(filename, writer=writer)
        plt.close()
        
        print(f"✓ Animation saved successfully!")
    
    def plot_snapshots(this, n_snapshots=6, filename='snapshots.png'):
        """Create snapshot plots at different times."""
        n_data = len(this.data)
        indices = np.linspace(0, n_data-1, n_snapshots, dtype=int)
        
        n_cols = 3
        n_rows = math.ceil(n_snapshots / n_cols)
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten() if n_snapshots > 1 else [axes]
        
        all_y = [this.data[i][1].p_y for i in range(n_data)]
        y_min = min([y.min() for y in all_y]) - 0.1
        y_max = max([y.max() for y in all_y]) + 0.1
        
        for idx, time_idx in enumerate(indices):
            ax = axes[idx]
            t, state = this.data[time_idx]
            
            ax.plot(state.p_x, state.p_y, 'b-', linewidth=2.5)
            ax.plot(state.p_x[1:-1], state.p_y[1:-1], 'ko', markersize=8)
            ax.plot([state.p_x[0], state.p_x[-1]], 
                   [state.p_y[0], state.p_y[-1]], 
                   'ro', markersize=12)
            
            ax.set_xlabel('x (m)', fontsize=10)
            ax.set_ylabel('y (m)', fontsize=10)
            ax.set_title(f't = {t:.3f} s', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
            ax.set_xlim(-0.05, this.system.l_cord + 0.05)
            ax.set_ylim(y_min, y_max)
        
        for idx in range(n_snapshots, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Snapshots saved to {filename}")