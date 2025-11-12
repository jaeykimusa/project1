# rk4.py

# Solves second-order ODEs using fourth-order Runge-Kutta method.
# Author: Jaey Kim
# Date: 10/01/2025


import numpy as np
import matplotlib.pyplot as plt  # <-- import matplotlib for plotting
from math_utils import StateVec

class RK4:

    def __init__(
            this, 
            function: callable, 
            y_0: StateVec, 
            x_0: float,
            h: float
        ):
        # existing initialization...
        this.f = function
        this.y = y_0
        this.x_0 = x_0
        this.x = this.x_0
        # this.x_lb = x_lb
        # this.x_ub = x_ub
        this.h = h
        # this.total_steps = int((x_ub - x_lb) / h)
        # this.current_step = 0
        
        # # Initialize lists to store values for plotting
        # this.x_values = [x_lb]
        # this.y1_values = [y1_0]
        # this.y2_values = [y2_0]

    def step(this):
        h = this.h
        x = this.x
        y = this.y
        f = this.f
        
        n = y.n

        if x == this.x_0:
            k1 = f(x, y, True)
            k2 = f(x + h/2, StateVec(n=n, x_init=(y.x + (1/2)*k1.x*h)), True)
            k3 = f(x + h/2, StateVec(n=n, x_init=(y.x + (1/2)*k2.x*h)), True)
            k4 = f(x + h, StateVec(n=n, x_init=y.x + k3.x*h), True)
        else:
            k1 = f(x, y, False)
            k2 = f(x + h/2, StateVec(n=n, x_init=(y.x + (1/2)*k1.x*h)), False)
            k3 = f(x + h/2, StateVec(n=n, x_init=(y.x + (1/2)*k2.x*h)), False)
            k4 = f(x + h, StateVec(n=n, x_init=y.x + k3.x*h), False)

        this.x += h
        this.y = StateVec(n=n, x_init=(this.y.x + (1/6)*(k1.x + 2*k2.x + 2*k3.x + k4.x)*h))

        return this.y


    # def getValues(this):
    #     return this.y1, this.y2

    # def printStep(this):
    #     '''
    #     Prints the result of a single RK4 step.

    #     Parameters:
    #         None
    #     Returns:
    #         None
    #     '''
    #     print("-"*15, "Step", this.current_step, "-"*15)
    #     print(f" x_{this.current_step} = {this.x:.9f}")
    #     print(f" y1(x_{this.current_step}) = {this.y1:.9f}")
    #     print(f" y2(x_{this.current_step}) = {this.y2:.9f}\n")
    

    # def solve(this):
    #     '''
    #     Solves to compute and print the problem results.

    #     Parameters:
    #         None
    #     Returns:
    #         None
    #     '''
    #     this.printStep()
    #     while(this.current_step < this.total_steps):
    #         this.step()
    #         this.printStep()
    
    # def plot(this):
    #     """
    #     Plots x vs y1 and x vs y2 on two separate subplots.
    #     """
    #     plt.figure(figsize=(10, 5))

    #     # Plot x vs y1
    #     plt.subplot(1, 2, 1)
    #     plt.plot(this.x_values, this.y1_values, label='y1(x)', color='b')
    #     plt.xlabel('Time (s)')
    #     plt.ylabel('Olive oil height in container (m)')
    #     plt.title('Plot of y1 vs x')
    #     plt.grid(True)
    #     plt.legend()

    #     # Plot x vs y2
    #     plt.subplot(1, 2, 2)
    #     plt.plot(this.x_values, this.y2_values, label='y2(x)', color='r')
    #     plt.xlabel('Time (s)')
    #     plt.ylabel('Plive oil height in funnel (m)')
    #     plt.title('Plot of y2 vs x')
    #     plt.grid(True)
    #     plt.legend()

    #     plt.tight_layout()
    #     # plt.show()
    #     plt.savefig("funnel0.02.png")