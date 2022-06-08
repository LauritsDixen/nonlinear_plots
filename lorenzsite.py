import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


class RK4():
    def __init__(self, inits, eqs, h):
        # inits is an n-dimensional array
        # eqs is an iterable of functions taking n numbers as inputs
        self.vals = inits
        self.eqs = eqs
        self.h = h
        self.records = inits

    def diff(self, vals):
        return np.array([d(vals) for d in self.eqs])

    def step(self):
        k1 = self.diff(self.vals)
        k2 = self.diff(self.vals + self.h*k1/2)
        k3 = self.diff(self.vals + self.h*k2/2)
        k4 = self.diff(self.vals + self.h*k3)
        self.vals = self.vals + self.h/6*(k1 + 2*k2 + 2*k3 + k4)
        self.records = np.vstack((self.records, self.vals))

@st.cache
def run_lorenz(timesteps, stepsize, inits, funcs):
    solver = RK4(inits, funcs, stepsize)

    for _ in range(timesteps): 
        solver.step()
    return solver.records

def plot_lorenz(r, azim):
    fig = plt.figure(figsize=(16,8), constrained_layout=True)
    ax = fig.gca(projection='3d')

    ax.axis('off')
    ax.view_init(elev=10., azim=azim)

    ax.plot3D(r[:,0],r[:,1],r[:,2], c='red', lw=0.6, clip_box=(0.1,0.1,0.1,0.1))
    return fig