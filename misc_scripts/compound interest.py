# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from matplotlib import style
from dash import Dash, dcc, html, Input, Output
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

external_stylesheets = ['/Users/v1att/projects/viz/assets/custom.css']

app = Dash(__name__,external_stylesheets=external_stylesheets)

def calculate(initial_investment, monthly_contribution, growth_rate, years):

    invested = 0 + initial_investment 
    earnings = 0
    total = invested + earnings
    
    records = dict(Invested=[], Earnings=[], Year=[], Total=[])

    for m in range(years*12):
        # Monthly yeild 
        dividend = total * growth_rate/12

        # Updating values
        invested += monthly_contribution
        earnings += dividend
        total += monthly_contribution + dividend

        # Record
        records['Invested'].append(invested)
        records['Earnings'].append(earnings)
        records['Total'].append(total)
        records['Year'].append((m+1)/12)

    return records

def make_fig(records):
    # Init fig
    fig = make_subplots(rows=1, cols=2, column_widths=[0.8, 0.1])
    
    # Handle year==0 with empty fig
    if len(records['Year']) == 0:
        return fig

    # Make lines in lineplot
    for line in ['Total', 'Invested', 'Earnings']:
        fig.add_trace(
            go.Scatter(x=records['Year'], y=records[line], mode='lines', name=line, line={'color':colors[line]}),
            row=1, col=1
    )
    # Update axes on line plot
    fig.update_layout(
        xaxis_title="Years",
        yaxis_title="Amount",
        margin=dict(l=20, r=20, t=20, b=20),
    )

    # Bar plot
    fig.add_trace(go.Bar(name='Payed', marker_color=colors['Invested'],
                         x=['Total'], y=(records['Invested'][-1], )),
                         row=1, col=2)   
    fig.add_trace(go.Bar(name='Earned', marker_color=colors['Earnings'],
                         x=['Total'], y=(records['Earnings'][-1], )), 
                         row=1, col=2, 
    )
    fig.update_layout(barmode='stack') # Make it stacked

    return fig

# Colors to use for plotting
colors = {'Total':'purple', 'Invested':'red', 'Earnings':'green'}


## APP HTML
app.layout = html.Div( children=[
    html.H1(
        children='Compound Interest Calculator',
        style={'textAlign': 'center', "margin-top": "20px", 'font-size': '36px',}
    ),

    html.Div([
        "Monthly Contribution: ",
        dcc.Input(id='contribution', value=100, type='number', style = {'font-size': '16px','width':'5%'}),
    ], style = {'margin-left':'10%'},
    ),
    html.Div([
        "Initial Investment: ",
        dcc.Input(id='initial', value=5000, type='number', style = {'font-size': '16px','width':'6%'}),
    ], style = {'margin-left':'10%'},
    ),
    html.Div([
        "Years: ",
        dcc.Input(id='years', value=10, type='number', style = {'font-size': '16px','width':'3%'}),
    ], style = {'margin-left':'10%'},
    ),
    html.Br(),
    html.Div([
        "  Growth Rate (%): ",
        dcc.Slider(4, 15, value=8, id='rate', marks={str(i): str(i) for i in range(4,16)}),
    ], style = {'width':'55%', 'textAlign':'center', 'margin-left':'10%',},
    ),
    html.Br(),
    dcc.Graph(
        id='graph',
        style = {'margin-left':'3%', 'margin-right':'3%'}
    ),
    html.Div(id='nums', style = {'margin-left':'80%',}),
])

@app.callback(
    Output('graph', 'figure'),
    Output('nums', 'children'),
    Input('initial', 'value'),
    Input('contribution', 'value'),
    Input('years', 'value'),
    Input('rate', 'value'))
def update_figure(initial, contrib, years, rate):
    initial = initial or 0
    contrib = contrib or 0
    years = years or 0
    
    # Calculate the results
    records = calculate(initial_investment=initial, 
                        monthly_contribution=contrib,
                        years=years,
                        growth_rate=rate/100)
    
    # Make the figure
    fig = make_fig(records)
    t = round(records['Total'][-1])

    outstring = f'Total: {t}'

    return fig, outstring


if __name__ == '__main__':
    app.run_server(debug=True)
