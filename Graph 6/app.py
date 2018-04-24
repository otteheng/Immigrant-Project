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
df = pd.read_csv(
    'https://raw.githubusercontent.com/otteheng/Immigrant-Project/master/Graph%206/clean_national_mexican_outcomes.csv?_sm_au_=iMVn4WnLFkrJ0btq')

outcomes = ["% less than High School diploma", "% with College Degree", "% with Health Insurance", "% Employed", "Median Individual Real Income"]

# Organize where items will be on the page
app.layout = html.Div([
    html.H3(
        children='Cross-Generational Differences between Mexican and Non-Mexican Immigrants, 1994-2016',
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
    html.Div([
        html.Div([
            dcc.Graph(id='indicator-graphic1',
                      config={'modeBarButtonsToRemove': ['sendDataToCloud', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'pan2d',
                                                         'zoom2d', 'resetScale2d'],
                              'displaylogo': False})
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='indicator-graphic2',
                      config={'modeBarButtonsToRemove': ['sendDataToCloud', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'pan2d',
                                                         'zoom2d', 'resetScale2d'],
                              'displaylogo': False})
        ], style={'width': '50%', 'display': 'inline-block'}),
    ]),
])


@app.callback(

    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('outcome-id', 'value')])
def outcome_mexican(outcome_id):
    dff = df[['year', 'wbhao_igen', outcome_id]]
    dff = dff[(dff.wbhao_igen == 'Mexican 1st Generation') | (dff.wbhao_igen == 'Mexican 2nd Generation')]

    lines = {}
    data = []

    m_max = dff[outcome_id].max()
    m_min = dff[outcome_id].min()
    n = df[['year', 'wbhao_igen', outcome_id]]
    n = n[(n.wbhao_igen == 'Non-Mexican 1st Generation') | (n.wbhao_igen == 'Non-Mexican 2nd Generation')]
    n_max = n[outcome_id].max()
    n_min = n[outcome_id].min()
    if m_max == n_max:
        df_max = m_max
    if m_min == n_min:
        df_min = m_min
    if m_max > n_max:
        df_max = m_max
    elif m_max < n_max:
        df_max = n_max
    if m_min > n_min:
        df_min = n_min
    elif m_min < n_min:
        df_min = m_min
    if df_min < 0.05:
        df_min = 0
    y_axis = {'title': '{0}'.format(outcome_id),
              'hoverformat': ',.2f',
              'range': [df_min, df_max]}

    legends = {'orientation': 'h', 'xanchor': 'center', 'x': '0.5', 'y': '-0.22'}

    generations = list(dff.wbhao_igen.unique())
    for gen in generations:
        if '1st' in gen:
            lines = dict(
                color=("#6b6ecf"),
                width=3)
        if '2nd' in gen:
            lines = dict(
                color=("#80b1d3"),
                width=3)
        trace = go.Scatter(
            x=dff[dff.wbhao_igen == gen]['year'],
            y=dff[dff.wbhao_igen == gen][outcome_id],
            mode='lines',
            name=gen,
            line=lines,
            opacity=0.8
        )

        data.append(trace)

    return {
        'data': data,
        'layout': go.Layout(
            title='Mexican',
            titlefont=dict(
                family='Georgia'),
            xaxis={'title': 'Year'},
            yaxis=y_axis,
            legend=legends
        )
    }


@app.callback(

    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('outcome-id', 'value')])
def outcome_nonmexican(outcome_id):
    dff = df[['year', 'wbhao_igen', outcome_id]]
    dff = dff[(dff.wbhao_igen == 'Non-Mexican 1st Generation') | (dff.wbhao_igen == 'Non-Mexican 2nd Generation')]

    lines = {}
    data = []

    n_max = dff[outcome_id].max()
    n_min = dff[outcome_id].min()
    m = df[['year', 'wbhao_igen', outcome_id]]
    m = m[(m.wbhao_igen == 'Mexican 1st Generation') | (m.wbhao_igen == 'Mexican 2nd Generation')]
    m_max = m[outcome_id].max()
    m_min = m[outcome_id].min()
    if m_max == n_max:
        df_max = m_max
    if m_min == n_min:
        df_min = m_min
    if n_max > m_max:
        df_max = n_max
    elif n_max < m_max:
        df_max = m_max
    if n_min > m_min:
        df_min = m_min
    elif n_min < m_min:
        df_min = n_min
    if df_min < 0.05:
        df_min = 0

    y_axis = {'title': '{0}'.format(outcome_id),
              'hoverformat': ',.2f',
              'range': [df_min, df_max]}
    legends = {'orientation': 'h', 'xanchor': 'center', 'x': '0.5', 'y': '-0.22'}

    generations = list(dff.wbhao_igen.unique())
    for gen in generations:
        if '1st' in gen:
            lines = dict(
                color=("#6b6ecf"),
                width=3)
        if '2nd' in gen:
            lines = dict(
                color=("#80b1d3"),
                width=3)
        trace = go.Scatter(
            x=dff[dff.wbhao_igen == gen]['year'],
            y=dff[dff.wbhao_igen == gen][outcome_id],
            mode='lines',
            name=gen,
            line=lines,
            opacity=0.8
        )

        data.append(trace)

    return {
        'data': data,
        'layout': go.Layout(
            title='Non-Mexican',
            titlefont=dict(
                family='Georgia'),
            xaxis={'title': 'Year'},
            yaxis=y_axis,
            legend=legends
        )
    }


# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)