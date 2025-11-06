# math_utils.py

import numpy as np

import numpy as np

class StateVec:
    def __init__(self, n: int = None, x_init: np.ndarray = None):
        """
        Either:
            StateVec(n)                 → create zero state for n nodes
        Or:
            StateVec(x_init=array)      → load state from array (size must be multiple of 4)
        """
        
        if x_init is not None:
            x_init = np.asarray(x_init, dtype=float)

            # verify valid shape
            if x_init.ndim != 1:
                raise ValueError("x_init must be a 1D array.")

            if x_init.size % 4 != 0:
                raise ValueError("x_init length must be divisible by 4.")

            self.n = x_init.size // 4
            self.x = x_init.copy()                # store flat vector
        else:
            if n is None:
                raise ValueError("Must provide n or x_init.")
            
            self.n = n
            self.x = np.zeros(4 * n, dtype=float)

        # Create the 4×n linked view
        self._view = self.x.reshape(4, self.n)

        # convenience linked views
        self.p_x = self._view[0]
        self.p_y = self._view[1]
        self.v_x = self._view[2]
        self.v_y = self._view[3]

    # same convenience accessors for node-wise position & velocity
    def p(self, i):
        return np.array([self.p_x[i], self.p_y[i]])

    def v(self, i):
        return np.array([self.v_x[i], self.v_y[i]])

    def print(self):
        print("state vector x:", self.x)
        print("shape:", self.x.shape)


class StateDerivativeVec:
    def __init__(this, n: int):
        """
        n = number of nodes
        State layout:
            x = [px_0..px_(n-1),  py_0..py_(n-1),  vx_0..vx_(n-1),  vy_0..vy_(n-1)]
        """
        this.n = n
        this.x = np.zeros(4 * n)              # flat storage
        this._view = this.x.reshape(4, n)     # (4, n) matrix view
        
        # define property views (do NOT assign new arrays)
        this.v_x = this._view[0]              # position x-coordinates
        this.v_y = this._view[1]              # position y-coordinates
        this.a_x = this._view[2]              # velocity x-components
        this.a_y = this._view[3]              # velocity y-components

    def print(this):
        print("state derivative vector x:", this.x)
        print("shape:", this.x.shape)

def getMagnitude(a, b=None):
    """
    If b is None:
        return ‖a‖    (magnitude of a)
    Else:
        return ‖b-a‖  (distance between points a and b)
    """
    a = np.asarray(a, dtype=float)

    if b is None:
        # magnitude of a single vector
        return np.linalg.norm(a)
    else:
        b = np.asarray(b, dtype=float)
        return np.linalg.norm(b-a)

def getUnitVector(a, b=None):
    """
    Returns the normal vector of the given vector.
    """
    a = np.asarray(a, dtype=float)

    if b is None:
        return a / np.linalg.norm(a)
    else:
        b = np.asarray(b, dtype=float)
        return (a-b) / np.linalg.norm(a-b)

