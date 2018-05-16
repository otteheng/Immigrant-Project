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
df = pd.read_csv('https://raw.githubusercontent.com/otteheng/Immigrant-Project/master/Graph%201/clean_national_topstates.csv')

states = list(df['state'].unique())

# Organize where items will be on the page
app.layout = html.Div([
        html.H3(
            children='Distribution of Immigrant Generation among Hispanics in the United States, 1994-2016',
            style={
                'textAlign': 'center', 'fontFamily' : 'Georgia'
            }
        ),
        html.Center([          
            html.Div([
                html.Div([html.P('Select State',id='state-title')],
                    style={'textAlign': 'center', 'fontFamily': 'Georgia'}),
                dcc.Dropdown(
                    id='state-id',
                    options=[{'label': i, 'value': i} for i in states],
                    value='National')
                ],style={'width': '50%','textAlign': 'center', 'fontFamily': 'Georgia', 'display': 'inline-block'}),        
            ]),
        html.Div([
                dcc.Graph(id='indicator-graphic1',
                          config={'modeBarButtonsToRemove': ['sendDataToCloud', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'pan2d', 
                                                             'zoom2d','resetScale2d'], 
                                'displaylogo': False})             
            ]),
    ])
@app.callback(

    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('state-id', 'value')])
def outcome_hispanic(state_id):
    dff = df[['year', 'wbhao_igen', 'state','Share of 1st Generation','Share of 2nd Generation', 'Share of 3rd Generation']]
    dff = dff[(dff.state == state_id) & (dff.wbhao_igen == 'Hispanic All')]

    lines = {}
    data = []
    y_axis = {'title': '% in {0}'.format(state_id), 
              'hoverformat': ',.2f',
              'range' : [0,1]}          
    legends={'orientation': 'h', 'xanchor': 'center', 'x': '0.5', 'y': '-0.22'}

    
    outcomes = ['Share of 1st Generation','Share of 2nd Generation', 'Share of 3rd Generation']
    for gen in outcomes:
        if '1st' in gen:
             lines = dict(
                 color = ("#6b6ecf"),
                 width = 3)
        if '2nd' in gen:
             lines = dict(
                 color = ("#80b1d3"),
                 width = 3)
        if '3rd' in gen:
             lines = dict(
                 color = ("#fdb462"),
                 width = 3)
        trace = go.Scatter(
            x = dff['year'],
            y = dff[gen],
            mode='lines',
            name = gen,
            line = lines,
            opacity = 0.8
            )
        
        data.append(trace)


    return {
        'data' : data,
        'layout' : go.Layout(
            titlefont=dict(
                        family='Georgia'),
            xaxis={'title': 'Year'},
            yaxis=y_axis,
            legend = legends
        )
    }

# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)