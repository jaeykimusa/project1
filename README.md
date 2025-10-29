# Bungee Cord Simulation Project

**Course:** MAE 495/589 - Computational Methods in Engineering  
**Instructor:** Dr. Hooman Tafreshi  
**Due:** October 16, 2025

## Project Overview

This project simulates a flexible cord (bungee cord) using two approaches:
1. **Mass-Spring-Damper (MSD) System** - Numerical simulation with 14 point masses
2. **1D Wave Equation** - Analytical solution using separation of variables

The project includes parameter tuning to match both approaches and simulations of traveling waves with time-dependent boundary conditions.

## Project Structure

```
.
├── bungee_msd_simulation.py      # Mass-spring-damper simulation
├── wave_equation_solver.py       # Wave equation analytical solver
├── compare_solutions.py          # Comparison and parameter tuning
├── traveling_wave_simulation.py  # Time-dependent BC simulation
├── run_all_simulations.py        # Main runner script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Requirements

### Python Version
- Python 3.8 or higher

### Dependencies
- numpy (numerical computations)
- scipy (ODE solver, integration)
- matplotlib (plotting and animation)
- ffmpeg (video generation)

## Installation

### 1. Install Python packages:
```bash
pip install -r requirements.txt --break-system-packages
```

### 2. Install ffmpeg (required for video generation):

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Usage

### Quick Start - Run All Simulations

To run all simulations and generate all outputs:

```bash
python run_all_simulations.py
```

This will:
1. Run the MSD simulation
2. Solve the wave equation
3. Compare both approaches
4. Simulate traveling waves

### Individual Simulations

#### 1. Mass-Spring-Damper Simulation
```bash
python bungee_msd_simulation.py
```
- Generates: `msd_snapshots.png`, `bungee_msd.mp4`

#### 2. Wave Equation Solution
```bash
python wave_equation_solver.py
```
- Generates: `wave_snapshots.png`, `wave_equation.mp4`

#### 3. Comparison and Tuning
```bash
python compare_solutions.py
```
- Generates: `comparison_snapshots.png`, `energy_plot.png`, `center_displacement.png`

#### 4. Traveling Wave Simulation
```bash
python traveling_wave_simulation.py
```
- Generates: `wave_propagation.png`, `traveling_wave.mp4`

## Output Files

All output files are saved to `/mnt/user-data/outputs/`:

### Images
- `msd_snapshots.png` - MSD simulation at different time steps
- `wave_snapshots.png` - Wave equation solution at different time steps
- `comparison_snapshots.png` - Side-by-side comparison of both methods
- `energy_plot.png` - Total energy vs time for MSD
- `center_displacement.png` - Center point displacement comparison
- `wave_propagation.png` - Space-time plot of traveling wave

### Videos
- `bungee_msd.mp4` - Animation of MSD simulation
- `wave_equation.mp4` - Animation of wave equation solution
- `traveling_wave.mp4` - Animation of traveling wave with time-dependent BC

## Parameter Tuning

To match the MSD simulation with the wave equation, adjust parameters in `compare_solutions.py`:

### Key Parameters

1. **Spring Constant (k_s)**
   - Controls wave speed: c ≈ sqrt(k_s/m) × dx
   - Typical range: 1000-5000 N/m
   - Higher values → faster waves

2. **Damping Constant (k_d)**
   - Controls energy dissipation
   - k_d = 0: Undamped (perfect match with wave equation)
   - k_d > 0: Damped (energy decays over time)
   - Typical range: 0-2 N·s/m

3. **Number of Fourier Modes (n_modes)**
   - For wave equation accuracy
   - Recommended: 50-100

### Example Parameter Sets

```python
# Undamped, moderate stiffness
k_s = 1000.0
k_d = 0.0

# Light damping, higher stiffness
k_s = 2000.0
k_d = 0.5

# Stiff, undamped
k_s = 5000.0
k_d = 0.0
```

## Mathematical Background

### Mass-Spring-Damper System

Newton's 2nd law for each point mass i:

```
ma_i = -k_s[(||p_i - p_{i-1}|| - l_r) × (p_i - p_{i-1})/||p_i - p_{i-1}||]
       -k_s[(||p_i - p_{i+1}|| - l_r) × (p_i - p_{i+1})/||p_i - p_{i+1}||]
       -k_d(u_i - u_{i-1}) - k_d(u_i - u_{i+1}) + mg
```

### 1D Wave Equation

```
∂²u/∂t² = c² ∂²u/∂x²
```

Boundary conditions:
- u(0,t) = 0 (fixed left end)
- u(L,t) = 0 (fixed right end)

Initial conditions:
- u(x,0) = f(x) (initial shape)
- ∂u/∂t(x,0) = g(x) (initial velocity)

Solution using separation of variables:
```
u(x,t) = Σ [A_n cos(ω_n t) + B_n sin(ω_n t)] sin(nπx/L)
```

where ω_n = nπc/L

## Customization

### Change Initial Conditions

In `bungee_msd_simulation.py` or `wave_equation_solver.py`:

```python
# Sine wave
def initial_shape(x):
    return 0.05 * np.sin(np.pi * x / L)

# Gaussian pulse
def initial_shape(x):
    return 0.1 * np.exp(-((x - 0.5) / 0.2)**2)

# Triangular pulse
def initial_shape(x):
    if x < L/2:
        return 0.1 * (2*x/L)
    else:
        return 0.1 * (2 - 2*x/L)
```

### Modify Time-Dependent Boundary Condition

In `traveling_wave_simulation.py`:

```python
# Change amplitude and frequency
wave_system.set_bc_parameters(amplitude=0.08, frequency=3.0)
```

## Report Guidelines

Your report should include:

1. **Introduction** - Brief problem description
2. **Methods** - Describe both MSD and wave equation approaches
3. **Results** - Show comparisons with figures
4. **Parameter Tuning** - Explain how you matched the solutions
5. **Traveling Wave** - Discuss the time-dependent BC case
6. **Conclusion** - Summary of findings

### Figure Requirements
- Proper captions and labels
- Units on all axes
- Legends where appropriate
- High resolution (300 dpi)
- No gray backgrounds or unnecessary frames
- Consistent fonts throughout

## Troubleshooting

### Import Errors
```bash
pip install numpy scipy matplotlib --break-system-packages
```

### Video Generation Fails
- Ensure ffmpeg is installed: `ffmpeg -version`
- Check file permissions in output directory

### Numerical Instability
- Reduce time step (increase n_points in simulate())
- Reduce spring constant (k_s)
- Increase damping (k_d)

### Solutions Don't Match
- Adjust k_s to change wave speed
- Set k_d = 0 for undamped comparison
- Increase n_modes for wave equation

## References

1. Project assignment document
2. Class lecture notes on wave equations
3. Numerical methods for ODEs (scipy.integrate.odeint documentation)

## Contact

For questions about the code implementation, refer to:
- Python documentation: https://docs.python.org/
- NumPy documentation: https://numpy.org/doc/
- SciPy documentation: https://docs.scipy.org/
- Matplotlib documentation: https://matplotlib.org/

## License

This code is for educational purposes only as part of MAE 495/589.

---

**Note:** While you can work together on the projects, what you submit should be your own original work.
