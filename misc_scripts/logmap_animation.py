import matplotlib.pyplot as plt
import imageio, os
import numpy as np

# Functions
def logmap(x, R):
    # Logistic Map
    return R*x*(1-x)

def simulate(n, init, R):
    x = init
    xs = [x]
    for _ in range(n):
        x = logmap(x, R)
        xs.append(x)
    return xs

def difference_data(r):
    xs = [r[0]]
    ys = [0]
    for i in range(1,len(r)):
        xs.append(r[i-1])
        ys.append(r[i])

        xs.append(r[i])
        ys.append(r[i])
    return xs, ys

def make_fig(result, R):
    
    fig, ax = plt.subplots(2)

    #ax[0].scatter(x=range(len()))

    ax[1].plot([0,1],[0,1], 'k')
    
    step=0.001
    xs = np.arange(0, 1, step=step)
    ys = np.apply_along_axis(logmap, 0, xs, R)
    ax[1].plot(xs,ys, 'k')

    xs, ys = difference_data(result)
    ax[1].plot(xs,ys, 'r')

    ax[1].set_xlim([0, 1])
    ax[1].set_ylim([0, 1])
    ax[1].set_title(f'R = {R}')
    
    plt.savefig(f'assets/pics/{R}.png')
    plt.close()
    return fig

def generate_pngs():
    for R in Rs:
        R = round(R,2)
        sim = simulate(n, init_x, R)
        make_fig(sim, R)

def make_gif():
    with imageio.get_writer('logmap.gif', mode='i') as writer:
        for R in Rs:
            R = round(R,2)
            image = imageio.imread(f'assets/pics/{R}.png')
            writer.append_data(image)

def cleanup():
    for R in Rs:
        R = round(R,2)
        os.remove(f'assets/pics/{R}.png')

# Vars
init_x = 0.1
n = 500
step=0.02
Rs = np.arange(0, 4+step, step=step)

generate_pngs()
make_gif()