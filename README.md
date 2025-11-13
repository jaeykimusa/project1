# Bungee Cord Simulation Project

**Course:** MAE 495/589 - Computational Methods in Engineering  
**Instructor:** Dr. Hooman Tafreshi  

## Project

This project simulates a flexible cord (bungee cord) using two approaches:
1. **Mass-Spring-Damper (MSD) System** - Numerical simulation with 14 point masses
2. **1D Wave Equation** - Analytical solution using separation of variables

## Implementation Structure

```
.
├── examples/
|      ├── sim_msd_simple_hanging_extended_nodes.py
|      ├── sim_msd_simple_hanging.py
|      └── sim_msd_sin_wave.py
├── point_masses_simulation.py
├── point_masses_system.py
├── math_utils.py
├── rk4.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

### Python Version
- Python 3.8 or higher

### Python Dependencies
- numpy
- scipy
- matplotlib

## Installation

### 1. Git Clone:
```bash
git clone https://github.com/jaeykimusa/project1.git
```

### 2. Install Python packages:

```bash
pip install -r requirements.txt --break-system-packages
```

## Usage

### Quick Start - Run All Simulations

To run simple MSD cord system hanging, try:

```bash
python -m examples.sim_msd_simple_hanging
```

<!--
This will:
1. Run the MSD simulation
2. Solve the wave equation
3. Compare both approaches
4. Simulate traveling waves
-->

### Individual Simulations

#### 1. Mass-spring-damper simulation with sin wave
```bash
python -m examples.sim_msd_sin_wave
```

#### 2. Mass-spring-damper simulation with extended point mass nodes
```bash
python -m examples.sim_msd_simple_hanging_extended_nodes.py
```

<!--
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
-->


## Results

#### Mass-spring-damper cord hanging with dynamics equation: 
<img src="https://github.com/user-attachments/assets/66f42944-0a7c-4a0c-9e13-13c96d69aea6" width="350">

#### Mass-spring-damper simulation with sin wave (gravity = 0)
<img src="https://github.com/user-attachments/assets/962b50e3-ac7c-4e8b-a987-199093d4afcc" width="350">

#### Mass-spring-damper simulation with extended point mass nodes (external forces in +y)
<img src="https://github.com/user-attachments/assets/1118a519-476f-4515-a5be-d63aee7a6e68" width="350">
