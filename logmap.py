# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import numpy as np
#import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


external_stylesheets = ['/Users/v1att/projects/viz/assets/custom.css']

app = Dash(__name__,external_stylesheets=external_stylesheets)

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

def make_fig(result, R):
    
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5])

    # Make lines in lineplot
    fig.add_trace(
        go.Scatter(x=list(range(len(result))), y=result, mode='markers'),
        row=1, col=1
    )

    # Update axes on line plot
    fig.update_layout(
        xaxis_title="Step",
        yaxis_title="Value",
        margin=dict(l=20, r=20, t=20, b=20),
    )

    
    
    fig.add_trace(
        go.Scatter(x=[0,1], y=[0,1], mode='lines', line={'color':'black'}),
        row=1, col=2
    )

    step=0.001
    xs = np.arange(0, 1, step=step)
    ys = np.apply_along_axis(logmap, 0, xs, R)
    fig.add_trace(
        go.Scatter(x=xs, y=ys, mode='lines', line={'color':'black'}),
        row=1, col=2
    )

    xs = [result[0]]
    ys = [0]
    for i in range(1,len(result)):
        xs.append(result[i-1])
        ys.append(result[i])

        xs.append(result[i])
        ys.append(result[i])
    fig.add_trace(
        go.Scatter(x=xs, y=ys, mode='lines', line={'color':'red'}),
        row=1, col=2
    )

    fig.update_xaxes(range=[0, 1],col=2)
    fig.update_yaxes(range=[0, 1])

    return fig

## APP HTML
app.layout = html.Div( children=[
    html.H1(
        children='Logistic Map',
        style={'textAlign': 'center', "margin-top": "20px", 'font-size': '36px',}
    ),

    html.Div([
        "Time steps: ",
        dcc.Input(id='steps', value=50, type='number', style = {'font-size': '16px','width':'5%'}),
    ], style = {'margin-left':'10%'},
    ),
    html.Div([
        "Initial Value: ",
        dcc.Input(id='initial', value=0.2, type='number', style = {'font-size': '16px','width':'6%'}),
    ], style = {'margin-left':'10%'},
    ),
    html.Div([
        "R: ",
        dcc.Input(id='R', value=3.1, type='number', style = {'font-size': '16px','width':'8%'}),
    ], style = {'margin-left':'10%'},
    ),
    html.Br(),
    dcc.Graph(
        id='graph',
        style = {'margin-left':'3%', 'margin-right':'3%'}
    ),
    html.Div(id='end', style = {'margin-left':'80%',}),
])

@app.callback(
    Output('graph', 'figure'),
    Output('end', 'children'),
    Input('steps', 'value'),
    Input('initial', 'value'),
    Input('R', 'value'))
def update_figure(n, init, R):
    n = n or 0
    init = init or 0
    R = R or 0
    
    # Calculate the results
    result = simulate(n, init, R)
    
    # Make the figure
    fig = make_fig(result, R)
    t = round(result[-1],5)
    #t = sum(result)/len(result)

    outstring = f'Ended at: {t}'

    return fig, outstring


if __name__ == '__main__':
    app.run_server(debug=True)
