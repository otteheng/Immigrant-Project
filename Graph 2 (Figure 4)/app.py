# Dependencies for project
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd
from dash.dependencies import Input, Output, State
import flask
import os
from random import randint

# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# df = append
df = pd.read_csv('https://raw.githubusercontent.com/otteheng/Immigrant-Project/master/Graph%202/clean_national_topstates.csv')

states = list(df['state'].unique())
outcomes = ["% with Health Insurance"]

# Organize where items will be on the page
app.layout = html.Div([
        html.H3(
            children='Cross-Generational Differences in Health Insurance Coverage among Hispanics, 1994-2016',
            style={
                'textAlign': 'center', 'fontFamily' : 'Georgia'
            }
        ),
        html.Div([
                html.Center([          
                    html.Div([
                        html.Div([html.P('Select State',id='state-title1')],
                            style={'textAlign': 'center', 'fontFamily': 'Georgia'}),
                        dcc.Dropdown(
                            id='state-id1',
                            options=[{'label': i, 'value': i} for i in states],
                            value='National')
                        ],style={'width': '40%','textAlign': 'center', 'fontFamily': 'Georgia', 'display': 'inline-block'}),        
                    ]),

            dcc.Graph(id='indicator-graphic1',
                      config={'modeBarButtonsToRemove': ['sendDataToCloud', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'pan2d', 
                                                         'zoom2d','resetScale2d'], 
                            'displaylogo': False}),                
            ]),
        ])
@app.callback(

    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('state-id1', 'value')])
def outcome_time_series1(state_id):
    dff = df[['year', 'wbhao_igen', 'state','% with Health Insurance']]
    dff = dff[dff['state'] == state_id]
    
    lines = {}
    data = []
    y_axis = {}
    legends={'orientation': 'h', 'xanchor': 'center', 'x': '0.5', 'y': '-0.22'}
    
    # Show three lines for each output
    generation = ['White All','Hispanic All', 'Hispanic 1st Generation', 'Hispanic 2nd Generation', 
                  'Hispanic 3rd Generation']
    for gen in generation:
        if '1st' in gen:
             lines = dict(
                 color = ("#6b6ecf"),
                 width = 2,
                 dash = 'dash')
        if '2nd' in gen:
             lines = dict(
                 color = ("#80b1d3"),
                 width = 2,
                 dash = 'dash')              
        if '3rd' in gen:
             lines = dict(
                 color = ("#fdb462"),
                 width = 2,
                 dash = 'dash')
        if 'White All' in gen:
              lines = dict(
                 color = ("#333333"),
                 width = 3)
        if 'Hispanic All' in gen:
               lines = dict(
                 color = ("#fb8072"),
                 width = 3)
        trace = go.Scatter(
            x = dff[dff['wbhao_igen']==gen]['year'],
            y = dff[dff['wbhao_igen']==gen]['% with Health Insurance'],
            mode='lines',
            name = gen,
            line = lines,
            opacity = 0.8
            )
        
        data.append(trace)
    y_axis = {'title': '{0}'.format('% with Health Insurance'), 
              'hoverformat': ',.2f'}  
    return {
        'data' : data,
        'layout' : go.Layout(
            xaxis={'title': 'Year'},
            yaxis=y_axis,
            legend=legends,
        )
    }

# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)