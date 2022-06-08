import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def logmap(x, R):
    # Logistic Map
    return R*x*(1-x)

@st.cache
def logmap_sim(n, init, R):
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
    return xs[st.session_state.n_trans*2:], ys[st.session_state.n_trans*2:]

def logmap_plot(result, R):
    # Setting up fig
    fig, ax = plt.subplots(1,2, figsize=(14, 7))
    
    # Time domain plot
    ax[0].set_title('Point plot')
    ax[0].set_ylim([0, 1])
    ax[0].scatter(x=range(st.session_state.n_trans, len(result)),y=result[st.session_state.n_trans:], c='k', s=7)

    # Setup difference plot
    ax[1].set_xlim([0, 1])
    ax[1].set_ylim([0, 1])
    ax[1].set_title('Cobweb plot')

    # Plot stable line
    ax[1].plot([0,1],[0,1], 'k')
    
    # Calc and plot parabola
    step = 0.02
    xs = np.arange(0, 1+step, step=step)
    ys = np.apply_along_axis(logmap, 0, xs, R)
    ax[1].plot(xs,ys, 'k')

    # Difference line
    xs, ys = difference_data(result)    
    ax[1].plot(xs, ys, 'r')
    if abs(xs[0]-xs[-1]) < 0.001:
        ax[1].plot(xs[0], ys[0], 'or', markersize=1)
    
    # Make fig
    st.pyplot(fig)