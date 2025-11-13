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
        this.f = function
        this.y = y_0
        this.x_0 = x_0
        this.x = this.x_0
        this.h = h

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