import matplotlib.pyplot as plt
import itertools
import numpy as np


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

n = 1000
transient = 700

rmin = 3.4
rmax = 3.8
step = 0.0001

x0 = 0.2

fig, ax = plt.subplots()
ax.set_ylim([0,1])

for r in np.arange(rmin,rmax,step):
    print(r)
    res = simulate(n, x0, r)
    x = list(itertools.repeat(r,n-transient))
    ax.scatter(x=x,y=res[transient+1:],alpha=0.02,s=0.05,c='k',marker='o')

fig.show()

plt.savefig('bifurs.svg', format='svg', dpi=96)