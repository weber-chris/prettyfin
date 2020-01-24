import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from pathlib import Path
import os
import json
import pandas as pd
import time

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

folder_preprocessed_data = Path(os.getcwd()) / 'data' / 'preprocessed'
df_ausgaben = pd.read_csv(folder_preprocessed_data / 'df_ausgaben_all_merged.csv', index_col=0)
# df_einnahmen = pd.read_csv(folder_preprocessed_data / 'df_einnahmen_all.csv', index_col=0)
min_year = df_ausgaben['year'].min()
max_year = df_ausgaben['year'].max()
year_ticks = {str(y): str(y) for y in df_ausgaben['year'].unique()}
init_year = 1991
cantons = df_ausgaben['canton'].unique()

with open(folder_preprocessed_data / 'funkt_id_map.json', 'r') as file:
    funkt_id_map = json.load(file)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # dcc.Graph(id='graph-with-slider', style={"width": "100%", "display": "inline-block"}),
    dcc.Graph(id='graph-bubbles', style={"width": "100%", "display": "inline-block"}),
    dcc.Slider(
        id='year-slider',
        min=min_year,
        max=max_year,
        value=init_year,
        marks=year_ticks,
        updatemode='drag',
        step=None
    ),
    dcc.Dropdown(
        id="x-axis-dropdown",
        options=[{'label': cat[1], 'value': cat[0]} for cat in funkt_id_map.items()],
        value='0', multi=False, style={'width': '50%', 'display': 'inline-block'}),
    dcc.Dropdown(
        id="y-axis-dropdown",
        options=[{'label': cat[1], 'value': cat[0]} for cat in funkt_id_map.items()],
        value='1', multi=False, style={'width': '50%', 'display': 'inline-block'}),
    html.Button(html.P('Start', id='start-button-text'), id='start-button'),

    dcc.Interval(id="interval", disabled=True, interval=1500),
    html.P(id="output"),
])


@app.callback(Output('start-button-text', 'children'), [Input("interval", "disabled")])
def change_button_text(disabled):
    if disabled:
        return 'Start'
    else:
        return 'Stop'


# @app.callback(Output("output", "children"), [Input("interval", "n_intervals")])
# def display_count(n):
#     return f"Interval has fired {n} times"


@app.callback([Output('year-slider', 'value'), Output("interval", "disabled")],
              [Input("interval", "n_intervals"), Input("start-button", "n_clicks")],
              [State('year-slider', 'value'),
               State("interval", "disabled")])
def slide_adjust(n_intervals, n_clicks, slider_year, disabled):
    ctx = dash.callback_context

    if ctx.triggered[0]['prop_id'] == 'interval.n_intervals':
        print('interval')
        if disabled is not None:
            if not disabled:
                slider_year += 1
            print(slider_year)
            if slider_year > max_year:
                return dash.no_update, True
            else:
                return slider_year, dash.no_update
        else:
            return dash.no_update, dash.no_update

    if ctx.triggered[0]['prop_id'] == 'start-button.n_clicks':
        print('button')
        if n_clicks:
            interval_status = not disabled
        else:
            return dash.no_update, dash.no_update

        return dash.no_update, interval_status


@app.callback(
    Output('graph-bubbles', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_bubble(x_axis, y_axis, selected_year):
    print('update_bubble')

    df_filtered = df_ausgaben[df_ausgaben.year == selected_year]
    traces = []
    for canton in cantons:
        df_canton = df_filtered[df_filtered['canton'] == canton]
        traces.append(dict(
            x=df_canton[x_axis],
            y=df_canton[y_axis],
            text=df_canton['canton'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': df_canton['population'] * 0.0001,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=canton
        ))

    fig = {
        'data': traces,
        'layout': dict(
            xaxis={'title': funkt_id_map[x_axis], 'range': [df_ausgaben[x_axis].min(), df_ausgaben[x_axis].max()]},
            yaxis={'title': funkt_id_map[y_axis], 'range': [df_ausgaben[y_axis].min(), df_ausgaben[y_axis].max()]},
            margin={'l': 60, 'b': 40, 't': 10, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            transition={'duration': 1000},
        )}

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
