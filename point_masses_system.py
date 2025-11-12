from math_utils import StateVec
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