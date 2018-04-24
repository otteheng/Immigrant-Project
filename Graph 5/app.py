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

# df = age
df = pd.read_csv(
    'https://raw.githubusercontent.com/otteheng/Immigrant-Project/master/Graph%205/clean_national_first_age.csv')

outcomes = ['% less than High School diploma', '% with College Degree', '% with Health Insurance', '% Employed', 'Median Individual Real Income']

# Organize where items will be on the page
app.layout = html.Div([
    html.H3(
        children='Distribution of Immigrant Generation Nationally by Age groups, 1994-2016',
        style={
            'textAlign': 'center', 'fontFamily': 'Georgia'
        }
    ),
    html.Center([
        html.Div([
            html.Div([html.P('Select Outcome', id='outcome-title')],
                     style={'textAlign': 'center', 'fontFamily': 'Georgia'}),
            dcc.Dropdown(
                id='outcome-id',
                options=[{'label': i, 'value': i} for i in outcomes],
                value='% less than High School diploma')
        ], style={'width': '50%', 'textAlign': 'center', 'fontFamily': 'Georgia', 'display': 'inline-block'}),
    ]),
    dcc.Graph(id='indicator-graphic',
              config={'modeBarButtonsToRemove': ['sendDataToCloud', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'pan2d',
                                                 'zoom2d', 'resetScale2d'],
                      'displaylogo': False}),
    html.Div([
        html.I('Click item in legend once to remove from graph, click item again to show item again. Double click \
                   to isolate item. Double click again to show all items.', id='below-graph-text')],
        style={'textAlign': 'center', 'fontFamily': 'Georgia', 'fontSize': '11'})
])


@app.callback(

    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('outcome-id', 'value')])
def outcome_hispanic(outcome_id):
    dff = df[['year', 'age_arrive_cat', outcome_id]]

    lines = {}
    data = []
    y_axis = {'title': '{0}'.format(outcome_id),
              'hoverformat': ',.2f'}
    legends = {'orientation': 'h', 'xanchor': 'center', 'x': '0.5', 'y': '-0.22'}

    generation = list(dff['age_arrive_cat'].unique())
    for gen in generation:
        if 'younger than 10' in gen:
            lines = dict(
                color=("#6b6ecf"),
                width=2,
                dash='dash')
        if 'between 10 and 18' in gen:
            lines = dict(
                color=("#80b1d3"),
                width=2,
                dash='dash')
        if 'older than 18' in gen:
            lines = dict(
                color=("#fdb462"),
                width=2,
                dash='dash')
        if 'Second' in gen:
            lines = dict(
                color=("#fb8072"),
                width=3)
        if 'White' in gen:
            lines = dict(
                color=("#333333"),
                width=3)
        trace = go.Scatter(
            x=dff[dff.age_arrive_cat == gen]['year'],
            y=dff[dff.age_arrive_cat == gen][outcome_id],
            mode='lines',
            name=gen,
            line=lines,
            opacity=0.8
        )

        data.append(trace)

    return {
        'data': data,
        'layout': go.Layout(
            xaxis={'title': 'Year'},
            yaxis=y_axis,
            legend=legends
        )
    }


# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)