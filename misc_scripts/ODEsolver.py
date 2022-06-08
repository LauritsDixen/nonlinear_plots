# ODE Solver
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import imageio, os

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
        

sigma = 10
beta = 8/3
rho = 28

dx = lambda v : sigma*(v[1]-v[0])
dy = lambda v : v[0]*(rho-v[2])-v[1]
dz = lambda v : v[1]*v[0]-beta*v[2]

inits = np.array([10,10,10])
            
def run_sim(timesteps, stepsize):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    solver = RK4(inits, (dx, dy, dz), stepsize)

    for _ in range(timesteps): 
        solver.step()
    #print(solver.records.shape)
    #ax.plot(solver.records[:,0],solver.records[:,1])
    ax.plot3D(solver.records[:,0],solver.records[:,1],solver.records[:,2],'gray')
    return fig

#fig = run_sim(30000, 0.01)
#plt.show()

def get_vector(x, i, tau, m):
    return tuple(x[i+tau*dim] for dim in range(m))

def reconstruction(x, tau, m):
    latest_index = len(x) - tau*(m-1)
    out = [get_vector(x, i, tau, m) for i in range(latest_index)]
    return out

def plot_taus(taus):
    fig, axes = plt.subplots(2, 4, sharex=True, sharey=True)

    
    m = 9

    for i, tau in enumerate(taus):
        r = reconstruction(data, tau, m)
        unzipped = list(zip(*r))

        index = int(i>3), i%4
        ax = axes[index]
        ax.set_title(f'Tau = {tau}')
        ax.plot(unzipped[0],unzipped[1], linewidth=0.1)
        
    plt.show()


data = np.loadtxt('/Users/v1att/projects/viz/assets/amplitude.dat')
taus = [2**i for i in range(8)]
taus = range(1,9)
plot_taus(taus)

def make_figname(var):
    return f'{pic_folder}/{var}.png'

def make_fig(r, tau):
    unzipped = list(zip(*r))

    fig, ax = plt.subplots()
    ax.plot(unzipped[0],unzipped[1], linewidth=0.1)

    #ax.set_xlim([0, 1])
    #ax.set_ylim([0, 1])
    ax.set_title(f'Tau = {tau}')
    plt.savefig(make_figname(tau))
    plt.close()
    return fig

def generate_pngs(varlist):
    for var in varlist:
        if not Path(make_figname(var)).is_file():
            print(f'making : {make_figname(var)}')
            r = reconstruction(data, var, m)
            make_fig(r, var)

def make_gif(gifname, varlist):
    with imageio.get_writer(gifname, mode='i') as writer:
        for var in varlist:
            image = imageio.imread(make_figname(var))
            writer.append_data(image)

def cleanup(varlist):
    for var in varlist:
        os.remove(make_figname(var))

# # Vars
# pic_folder = '/Users/v1att/projects/viz/assets/pics'
# outfilename = '/Users/v1att/projects/viz/reconstruction.gif'
# data = np.loadtxt('/Users/v1att/projects/viz/assets/amplitude.dat')
# m = 6
# step = 1
# taus = np.arange(1, 350+step, step=step)

# generate_pngs(taus)
# make_gif(outfilename, taus)