import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
        value='0', multi=False),
    dcc.Dropdown(
        id="y-axis-dropdown",
        options=[{'label': cat[1], 'value': cat[0]} for cat in funkt_id_map.items()],
        value='1', multi=False),
    html.Button('Start', id='start-button'),
])


@app.callback(
    Output('graph-bubbles', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('year-slider', 'value')])
def update_bubble(x_axis, y_axis, selected_year):
    start = time.time()
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
                'size': df_canton['population']*0.0001,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=canton
        ))

    fig =  {
        'data': traces,
        'layout': dict(
            xaxis={'title': funkt_id_map[x_axis], 'range': [df_ausgaben[x_axis].min(), df_ausgaben[x_axis].max()]},
            yaxis={'title': funkt_id_map[y_axis], 'range': [df_ausgaben[y_axis].min(), df_ausgaben[y_axis].max()]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition={'duration': 1000},
        )}
    end = time.time()
    print(end-start)
    return fig


# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     [Input('x-axis-dropdown', 'value'), Input('y-axis-dropdown', 'value')])
# def update_figure(x_axis, y_axis):
#     start = time.time()
#     fig = px.scatter(df_ausgaben[[x_axis, y_axis,'canton']], x=x_axis, y=y_axis, animation_frame=df_ausgaben.index, animation_group="canton",
#                      color="canton", hover_name="canton",
#                      log_x=True, size_max=55, range_x=[0.9*df_ausgaben[x_axis].min(), 1.1*df_ausgaben[x_axis].max()],
#                      range_y=[0.9*df_ausgaben[y_axis].min(), 1.1*df_ausgaben[y_axis].max()])
#     # fig.update_layout(showlegend=False)
#     end = time.time()
#     print(end-start)
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)
