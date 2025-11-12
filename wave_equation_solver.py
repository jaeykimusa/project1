import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class WaveEquationSolver:
    def __init__(self, L, c, dx, dt, sim_time):
        """
        Solve 1D wave equation using finite difference method
        ∂²u/∂t² = c²(∂²u/∂x²)
        
        Parameters:
        L: length of string
        c: wave speed
        dx: spatial step
        dt: time step
        sim_time: total simulation time
        """
        self.L = L
        self.c = c
        self.dx = dx
        self.dt = dt
        self.sim_time = sim_time
        
        # Grid points
        self.nx = int(L/dx) + 1
        self.x = np.linspace(0, L, self.nx)
        
        # Check CFL condition for stability
        self.r = c * dt / dx
        if self.r > 1:
            print(f"Warning: CFL condition violated! r = {self.r} > 1")
            print("Solution may be unstable. Consider reducing dt or increasing dx")
        
        # Initialize solution arrays
        self.u_prev = np.zeros(self.nx)  # u at t-dt
        self.u_curr = np.zeros(self.nx)  # u at t
        self.u_next = np.zeros(self.nx)  # u at t+dt
        
        self.time = 0
        
    def set_initial_conditions(self, initial_shape_func, initial_velocity_func):
        """
        Set initial displacement and velocity
        
        Parameters:
        initial_shape_func: function u(x, t=0)
        initial_velocity_func: function du/dt(x, t=0)
        """
        # Initial displacement
        self.u_prev = initial_shape_func(self.x)
        self.u_curr = initial_shape_func(self.x)
        
        # Apply boundary conditions
        self.u_prev[0] = 0
        self.u_prev[-1] = 0
        self.u_curr[0] = 0
        self.u_curr[-1] = 0
        
        # Use initial velocity to compute first time step
        # From Taylor series: u(t+dt) ≈ u(t) + dt*du/dt + 0.5*dt²*d²u/dt²
        # Using wave equation: d²u/dt² = c²*d²u/dx²
        v_init = initial_velocity_func(self.x)
        
        # Compute second derivative for initial condition
        d2u_dx2 = np.zeros(self.nx)
        for i in range(1, self.nx-1):
            d2u_dx2[i] = (self.u_curr[i+1] - 2*self.u_curr[i] + self.u_curr[i-1]) / self.dx**2
        
        # First time step using initial conditions
        self.u_prev = self.u_curr - self.dt * v_init + 0.5 * self.dt**2 * self.c**2 * d2u_dx2
        
    def step(self):
        """Advance solution by one time step using finite difference"""
        r2 = self.r**2
        
        # Update interior points using finite difference scheme
        for i in range(1, self.nx-1):
            self.u_next[i] = (2*(1-r2)*self.u_curr[i] + 
                             r2*(self.u_curr[i+1] + self.u_curr[i-1]) - 
                             self.u_prev[i])
        
        # Apply boundary conditions (fixed ends)
        self.u_next[0] = 0
        self.u_next[-1] = 0
        
        # Update arrays for next iteration
        self.u_prev[:] = self.u_curr
        self.u_curr[:] = self.u_next
        
        self.time += self.dt
        
        return self.u_curr.copy()
    
    def animate(self):
        """Create animation of wave equation solution"""
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Set up plot
        ax.set_xlim(0, self.L)
        ax.set_ylim(-0.35, 0.35)
        ax.set_xlabel('Position (m)')
        ax.set_ylabel('Displacement (m)')
        ax.set_title('1D Wave Equation Solution')
        ax.grid(True, linestyle=':', color='lightgray', alpha=0.7)
        
        line, = ax.plot(self.x, self.u_curr, 'b-', lw=2)
        time_text = ax.text(0.5, 0.95, f't = {self.time:.3f} s',
                           transform=ax.transAxes, ha='center', va='top',
                           bbox=dict(boxstyle="round,pad=0.3", 
                                   facecolor="white", edgecolor="black"))
        
        def update(frame):
            self.step()
            line.set_ydata(self.u_curr)
            time_text.set_text(f't = {self.time:.3f} s')
            return line, time_text
        
        n_frames = int(self.sim_time / self.dt)
        ani = animation.FuncAnimation(fig, update, frames=n_frames, 
                                    interval=1000*self.dt, blit=False)
        
        plt.tight_layout()
        plt.show()
        return ani


def main():
    # Parameters to match your MSD simulation
    L = 1.0  # Length of cord
    
    # You'll need to tune 'c' to match the wave speed from your MSD system
    # Wave speed c = sqrt(T/μ) where T is tension and μ is linear mass density
    # For your system: c ≈ sqrt(k_s * l_0 / m) where l_0 is rest length between masses
    
    n_m = 14  # number of masses (to match your MSD)
    m_total = 0.010 * n_m  # total mass
    mu = m_total / L  # linear mass density
    
    # Estimate wave speed from spring constant
    # This will need tuning to match your MSD results
    k_s = 1000
    l_0 = L / (n_m + 1)
    c = np.sqrt(k_s * l_0 / 0.010)  # Initial estimate
    
    print(f"Estimated wave speed: c = {c:.2f} m/s")
    
    # Discretization
    dx = L / 100  # Spatial resolution
    dt = 0.001   # Time step (ensure CFL condition: c*dt/dx < 1)
    sim_time = 10.0
    
    # Create solver
    solver = WaveEquationSolver(L, c, dx, dt, sim_time)
    
    # Define initial conditions (example: hanging under gravity)
    # Parabolic shape approximating gravitational sag
    def initial_shape(x):
        """Parabolic initial shape (like hanging cord)"""
        # u(x) = -a * x * (L - x) where a determines sag depth
        a = 1.0  # Adjust to match your MSD initial sag
        return -a * x * (L - x)
    
    def initial_velocity(x):
        """Initial velocity (typically zero for hanging cord)"""
        return np.zeros_like(x)
    
    # Set initial conditions
    solver.set_initial_conditions(initial_shape, initial_velocity)
    
    # Run animation
    ani = solver.animate()
    
    return solver, ani


if __name__ == "__main__":
    solver, ani = main()