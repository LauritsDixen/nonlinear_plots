import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from time import sleep

from logmapsite import logmap_sim, logmap_plot
from lorenzsite import run_lorenz, plot_lorenz

st.set_page_config(layout="wide")

def logmap_site():
    st.title('Logistic Map Explorer')
    st.text('The logistic map is a mapping function, given by the following equation:')
    st.latex(r'''x_{n+1} = R \left( 1-x_{n} \right) x_{n}''')
    st.text('It is a powerful example of a simple system showing complex behaviour.\nTry different values and see how the system reacts.')

    # Init values
    col1, col2 = st.columns(2)
    with col1:
        x0 = st.slider('Initial Value', 0., 1., 0.2, step=0.01)
        n = st.number_input('number of points', min_value=2, max_value=None, value=50, step=1, format='%i')
    with col2:
        R = st.slider('R', 0.0, 4., 3.27, step=0.01)
        n_trans = st.number_input('transient points', min_value=0, max_value=n, value=0, step=1, format='%i', key='n_trans')

    # Run the sim
    data = logmap_sim(n, x0, R)

    # Check for transience
    n_trans = st.session_state['n_trans']

    if 'n_trans' not in st.session_state:
        st.session_state['n_trans'] = n_trans

    # Plotting 
    logmap_plot(data, R)

def lorenz_site():
    # Top text
    st.title('Lorenz Attractor')

    st.text("The Lorenz system is a system of ordinary differential equations first studied by mathematician and Edward Lorenz. ")
    st.text("The differential equations are given by:")
    st.latex(r'''\frac{dx}{dt} = \sigma(y-x)''')
    st.latex(r'''\frac{dy}{dt} = x(\rho-z)-y''')
    st.latex(r'''\frac{dz}{dt} = xy-\beta z''')
    st.text("Here you can set the parameters of the system and see the different chaotic attractors it produces.")
    st.text("3D graphs are still a little funky in Streamlit, so bear with the large whitespace and clunky animation")


    # Values (userinput)    
    reset = st.button('Reset Values')
    if reset:
        st.session_state.sigma = 10
        st.session_state.beta = 8/3
        st.session_state.rho = 28

    col1, col2, col3 = st.columns(3)
    with col1:
        sigma = st.slider('Sigma', 0, 50, 10, step=1, key="sigma")
        animate = st.button('Rotate')
    with col2:
        beta = st.slider('Beta', 0., 10., 8/3, step=0.1, key="beta")
        loading_text = st.text('')
    with col3:
        rho = st.slider('Rho', 0, 100, 28, step=1, key="rho")
    
    # Predetermined values and functions
    dx = lambda v : sigma*(v[1]-v[0])
    dy = lambda v : v[0]*(rho-v[2])-v[1]
    dz = lambda v : v[1]*v[0]-beta*v[2]
    funcs = (dx, dy, dz)
    inits = np.array((1., 1., 1))
    timesteps = 10000
    stepsize = 0.005
    n_trans = 0

    # Run the sim and plot
    data = run_lorenz(timesteps, stepsize, inits, funcs)
    fig = plot_lorenz(data[n_trans:],0)
    lorenz_plot = st.pyplot(fig)

    if animate:
        figs = []
        loading_text = loading_text.text('Loading the figs to rotate')
        for azim in range(0,360,18):
            figs.append(plot_lorenz(data[n_trans:],azim))
        loading_text = loading_text.text('')
        for fig in figs:
            lorenz_plot = lorenz_plot.pyplot(fig)  
        animate = False


def main():
    page = st.sidebar.selectbox(
        "Select a Page",
        [
            "Logistic Map Explorer",
            "Lorenz Attractor"
        ]
    )
    if page == "Logistic Map Explorer":
        logmap_site()

    if page == "Lorenz Attractor":
        lorenz_site() 

main()