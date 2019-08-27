#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 20:23:00 2019

@author: tefirman
"""

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

def logFactorial(value):
    """ Returns the logarithm of the factorial of the value provided using Sterling's approximation """
    if all([value > 0,abs(round(value) - value) < 0.000001,value <= 34]):
        return float(sum(np.log(range(1,int(value) + 1))))
    elif all([value > 0,abs(round(value) - value) < 0.000001,value > 34]):
        return float(value)*np.log(float(value)) - float(value) + \
        0.5*np.log(2.0*np.pi*float(value)) - 1.0/(12.0*float(value))
    elif value == 0:
        return float(0)
    else:
        return float('nan')

def expectedWinnings(realBills,pctAnalyzed,detectionProb):
    probs = []
    winnings = []
    expected = []
    for fakeBills in range(301):
        numAnalyzed = round(pctAnalyzed*(realBills + fakeBills))
        choose_k = [np.exp(logFactorial(fakeBills) \
        - logFactorial(fakesAnalyzed) \
        - logFactorial(fakeBills - fakesAnalyzed) \
        + logFactorial(realBills) \
        - logFactorial(numAnalyzed - fakesAnalyzed) \
        - logFactorial(realBills - numAnalyzed + fakesAnalyzed))
        for fakesAnalyzed in range(max(numAnalyzed - realBills,0),min(numAnalyzed,fakeBills) + 1)]
        choose_k = [0 for ind in range(max(numAnalyzed - realBills,0))] + choose_k
        choose_k = np.array(choose_k)/sum(choose_k)
        probs.append(sum([choose_k[ind]*(1 - detectionProb)**ind for ind in range(len(choose_k))]))
        winnings.append(100*(realBills + fakeBills))
        expected.append(winnings[-1]*probs[-1])
    return expected

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Slider(
                id='real-bills',
                min=0,
                max=100,
                step=1,
                value=25,
                marks={
                    0:{'label': 'R: 0'},
                    25:{'label': '25'},
                    50: {'label': '50'},
                    75: {'label': '75'},
                    100: {'label': '100'}
                }
        )],
        style={'height':'30px','width':'90%','padding-left':'5%','padding-right':'5%','display':'inline-block'}),
        html.Div([
            dcc.Slider(
                id='pct-analyzed',
                min=0,
                max=100,
                step=1,
                value=5,
                marks={
                    0:{'label': 'a: 0%'},
                    25:{'label': '25%'},
                    50: {'label': '50%'},
                    75: {'label': '75%'},
                    100: {'label': '100%'}
                }
        )],
        style={'height':'30px','width':'90%','padding-left':'5%','padding-right':'5%','display':'inline-block'}),
        html.Div([
            dcc.Slider(
                id='detection-prob',
                min=0,
                max=100,
                step=1,
                value=25,
                marks={
                    0:{'label': 'p: 0%'},
                    25:{'label': '25%'},
                    50: {'label': '50%'},
                    75: {'label': '75%'},
                    100: {'label': '100%'}
                }
            )
        ],
        style={'height':'30px','width':'90%','padding-left':'5%','padding-right':'5%','display':'inline-block'}),
        html.Div(id='slider-output-container',style={'padding-left':'5%'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter'
        )
    ], style={'width': '96%', 'display': 'inline-block', 'padding': '0 20'})
])

@app.callback([dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),\
     dash.dependencies.Output('slider-output-container', 'children')],
    [dash.dependencies.Input('real-bills', 'value'),
     dash.dependencies.Input('pct-analyzed', 'value'),
     dash.dependencies.Input('detection-prob', 'value')])
def update_graph(real_bills,pct_analyzed,detection_prob):
    earnings = expectedWinnings(real_bills,pct_analyzed/100,detection_prob/100)
    return {
        'data': [go.Scatter(
            x = [ind for ind in range(len(earnings))],
            y = earnings,
            mode = 'lines+markers',
            marker= dict(size=6),
            name = 'Expected Earnings',
            line = dict(width=3,color='blue')
        ),
        go.Scatter(
            x = np.where(earnings == max(earnings))[0],
            y = [max(earnings)],
            mode = 'markers',
            marker= dict(size=10,color='red'),
            name = 'Maximum Earnings',
            line = dict(width=3,color='red')
        )],
        'layout': go.Layout(
            xaxis={
                'title':'# of Fake Bills'
            },
            yaxis={
                'title': 'Expected Earnings ($)',
                'type': 'linear'
            },
            margin={'l': 60, 'b': 80, 't': 10, 'r': 50},
            height=450,
            barmode='group',
            hovermode='closest'
        )
    }, 'R = ' + str(real_bills) + ', a = ' + str(pct_analyzed) + '%, p = ' + \
    str(detection_prob) + '%, Maximum Expected Earnings of $' + \
    str(round(max(earnings),2)) + ' at F = ' + str(np.where(earnings == max(earnings))[0][0])

if __name__ == '__main__':
    app.run_server()



