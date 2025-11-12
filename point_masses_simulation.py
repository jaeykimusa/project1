import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from point_masses_system import PointMassesSystem

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
        """
        Minimal, live animation with wall graphics, grid, and boxed time display
        """
        # --------- Figure / Axes (minimalist) ----------
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_aspect("equal", adjustable="box")
        
        # Initial positions from the current system state
        x0 = this.system.x
        px0, py0 = np.asarray(x0.p_x), np.asarray(x0.p_y)

        # Set bounds
        L = getattr(this.system, "l_cord", 1.0)
        pad = 0.05 * (L if np.isfinite(L) else 1.0)
        xmin, xmax = px0.min() - pad, px0.max() + pad
        ymin = -0.35
        ymax = 0.35
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        
        # --------- Add light gray dotted grid ---------
        ax.grid(True, linestyle=':', color='lightgray', linewidth=0.5, alpha=0.7)
        ax.set_axisbelow(True)  # Put grid behind other elements
        
        # Keep minimal tick marks for the grid
        ax.tick_params(axis='both', which='both', length=0, labelsize=8, colors='gray')
        
        # Optional: remove tick labels if you want just the grid
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])
        
        # Make spines light gray to match grid
        for sp in ax.spines.values():
            sp.set_color('lightgray')
            sp.set_linewidth(0.5)

        # --------- Simple wall hatching ---------
        wall_height = 0.12 * L
        n_lines = 6
        line_length = 0.03 * L
        
        # Left wall hatching
        for i in range(n_lines):
            y = -wall_height/2 + i * wall_height/(n_lines-1)
            ax.plot([px0[0] - line_length, px0[0]], 
                [y - line_length*0.5, y], 
                'k-', lw=1, zorder=5)
        
        # Right wall hatching  
        for i in range(n_lines):
            y = -wall_height/2 + i * wall_height/(n_lines-1)
            ax.plot([px0[-1], px0[-1] + line_length], 
                [y, y - line_length*0.5], 
                'k-', lw=1, zorder=5)
        
        # Vertical lines at attachment points
        ax.plot([px0[0], px0[0]], [-wall_height/2, wall_height/2], 'k-', lw=1.5, zorder=5)
        ax.plot([px0[-1], px0[-1]], [-wall_height/2, wall_height/2], 'k-', lw=1.5, zorder=5)

        # --------- Animation elements ---------
        # Line connects all points
        (line,) = ax.plot(px0, py0, "-", lw=0.8, color="black", zorder=3)
        
        # Scatter only shows middle masses (exclude endpoints)
        scat = ax.scatter(px0[1:-1], py0[1:-1], s=12, color="black", zorder=4)
        
        # --------- Time display with box at top center ---------
        time_text = ax.text(0.5, 0.95, f"t = {this.time:.3f} s",
                            transform=ax.transAxes, 
                            ha="center", va="top",
                            fontsize=10,
                            bbox=dict(boxstyle="round,pad=0.3", 
                                    facecolor="white", 
                                    edgecolor="black",
                                    linewidth=0.5))

        n_frames = int(round(this.sim_time / this.dt))

        def update(_i):
            this.system.step()
            this.time += this.dt
            x = this.system.x
            px, py = np.asarray(x.p_x), np.asarray(x.p_y)
            
            # Update line with all points
            line.set_data(px, py)
            
            # Update scatter with only middle points (exclude endpoints)
            scat.set_offsets(np.c_[px[1:-1], py[1:-1]])
            
            time_text.set_text(f"t = {this.time:.3f} s")
            return line, scat, time_text

        ani = animation.FuncAnimation(
            fig, update, frames=n_frames, interval=1000 * this.dt, blit=False
        )

        plt.tight_layout()
        plt.show()