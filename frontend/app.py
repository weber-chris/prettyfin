import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from pathlib import Path
import os
import json
import pandas as pd
import time

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

folder_preprocessed_data = Path(os.getcwd()) / 'data' / 'preprocessed'
df_ausgaben = pd.read_csv(folder_preprocessed_data / 'df_ausgaben_all_merged.csv', index_col=0)
# df_einnahmen = pd.read_csv(folder_preprocessed_data / 'df_einnahmen_all.csv', index_col=0)

with open(folder_preprocessed_data / 'funkt_id_map.json', 'r') as file:
    funkt_id_map = json.load(file)
with open(folder_preprocessed_data / 'iso_canton_map.json', 'r') as file:
    iso_canton_map = json.load(file)
with open(folder_preprocessed_data / 'population_id_map.json', 'r') as file:
    population_id_map = json.load(file)

min_year = df_ausgaben['year'].min()
max_year = df_ausgaben['year'].max()
year_ticks = {str(y): str(y) for y in df_ausgaben['year'].unique()}
init_year = 1991
cantons = df_ausgaben['canton'].unique()
cantons.sort()  # needed so that legend is alphabetical

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# because we use tabs,
# there will be callbacks specified to elements that are not initially in
# app.layout (if there are callbacks present in the other pages or tabs). that's why we set:
app.config.suppress_callback_exceptions = True
server = app.server

app.layout = html.Div([
    html.H1('Prettyfin'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Bubble Graph', value='tab-graph'),
        dcc.Tab(label='Line Graph', value='tab-line'),
        dcc.Tab(label='Map', value='tab-map'),
    ]),
    html.Div(id='tabs-content-example')
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-graph':
        return html.Div([
    # dcc.Graph(id='graph-with-slider', style={'width': '100%', 'display': 'inline-block'}),
    dcc.Graph(id='graph-bubbles', style={'width': '100%', 'height': '65vh'}),
    html.Div([

        html.Div([html.Button(html.P('Play', id='start-button-text', style={'width': '5%', }), id='start-button')],
                 style={'width': '6%'}),
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=min_year,
                max=max_year,
                value=init_year,
                marks=year_ticks,
                updatemode='drag',
                step=None
            )], style={'width': '90%'})],
        style={'display': 'flex', 'margin': '20px 0px 20px 0px', 'align-items': 'center'}),
    html.Div([
        html.Div([dcc.RadioItems(
            id='normalize-radio',
            options=[
                {'label': 'Absolute', 'value': 'absolute'},
                {'label': 'Normalized', 'value': 'normalized'}
            ],
            value='absolute'
        )], style={'width': '6%'}),
        html.Div([dcc.Dropdown(
            id='x-axis-dropdown',
            options=[{'label': cat[1], 'value': cat[0]} for cat in funkt_id_map.items()],
            value='0', multi=False, style={'width': '30vw'})]),
        html.Div([dcc.Dropdown(
            id='y-axis-dropdown',
            options=[{'label': cat[1], 'value': cat[0]} for cat in funkt_id_map.items()],
            value='1', multi=False, style={'width': '30vw'})]
        ),
        html.Div([dcc.Dropdown(
            id='size-dropdown',
            options=[{'label': cat[1], 'value': cat[0]} for cat in population_id_map.items()],
            value='population', multi=False, style={'width': '30vw'})]
        )
    ], style={'display': 'flex', 'align-items': 'center'}),

    dcc.Interval(id='interval', disabled=True, interval=1500),
], style={'width': '100%'})
    elif tab == 'tab-line':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])
    elif tab == 'tab-map':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

@app.callback(Output('start-button-text', 'children'), [Input('interval', 'disabled')])
def change_button_text(disabled):
    if disabled:
        return 'Play'
    else:
        return 'Stop'


# @app.callback(Output('output', 'children'), [Input('interval', 'n_intervals')])
# def display_count(n):
#     return f'Interval has fired {n} times'


@app.callback([Output('year-slider', 'value'), Output('interval', 'disabled')],
              [Input('interval', 'n_intervals'), Input('start-button', 'n_clicks')],
              [State('year-slider', 'value'),
               State('interval', 'disabled')])
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
     Input('size-dropdown', 'value'),
     Input('normalize-radio', 'value'),
     Input('year-slider', 'value')]
)
def update_bubble(x_axis, y_axis, bubble_size_dropdown, normalize, selected_year):
    print('update_bubble')

    df_filtered = df_ausgaben[df_ausgaben.year == selected_year]
    traces = []
    for canton in cantons:
        df_canton = df_filtered[df_filtered['canton'] == canton]

        if normalize == 'normalized':
            x_vals = min_max_normalization(df_canton,df_ausgaben, x_axis, canton)
            y_vals = min_max_normalization(df_canton,df_ausgaben, y_axis, canton)
        else:
            x_vals = df_canton[x_axis]
            y_vals = df_canton[y_axis]

        traces.append(dict(
            x=x_vals,
            y=y_vals,
            # x=df_canton[x_axis],
            # y=df_canton[y_axis],
            text=df_canton['canton'].apply(lambda x: iso_canton_map[x]),
            mode='markers',
            opacity=0.7,
            marker={
                'size': df_canton[bubble_size_dropdown] / df_ausgaben[bubble_size_dropdown].max() * 200,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=iso_canton_map[canton]
        ))

    if normalize == 'normalized':
        x_range = [0, 1]
        y_range = [0, 1]
    else:
        x_range = [df_ausgaben[x_axis].min(), df_ausgaben[x_axis].max()]
        y_range = [df_ausgaben[y_axis].min(), df_ausgaben[y_axis].max()]
    fig = {
        'data': traces,
        'layout': dict(
            xaxis={'title': {'text': funkt_id_map[x_axis], 'font': {'size': 24}},
                   'range': x_range},
            yaxis={'title': {'text': funkt_id_map[y_axis], 'font': {'size': 24}},
                   'range': y_range},
            margin={'l': 100, 'b': 80, 't': 10, 'r': 20},
            legend={'x': 1, 'y': 1, 'font': {'size': 13}},
            hovermode='closest',
            transition={'duration': 1000},
        )}

    return fig


def min_max_normalization(df_canton_year,df_all, axis, canton):
    df_canton_all = df_all[df_all['canton'] == canton][axis]
    x = (df_canton_year[axis] - df_canton_all.min()) / (df_canton_all.max() - df_canton_all.min())
    return x


if __name__ == '__main__':
    app.run_server(debug=True)
