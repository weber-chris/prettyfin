import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly_express as px
from pathlib import Path
import os
import json
import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

folder_preprocessed_data = Path(os.getcwd()).parent / 'data' / 'preprocessed'
df_ausgaben = pd.read_csv(folder_preprocessed_data / 'df_ausgaben_all.csv', index_col=0)
df_einnahmen = pd.read_csv(folder_preprocessed_data / 'df_einnahmen_all.csv', index_col=0)

with open(folder_preprocessed_data / 'funkt_id_map.json', 'r') as file:
    funkt_id_map = json.load(file)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider', style={"width": "100%", "display": "inline-block"}),
    # dcc.Dropdown(
    #     id="continent-dropdown",
    #     options=[{'label': 'Asia', 'value': 'Asia'}, {'label': 'Europe', 'value': 'Europe'},
    #              {'label': 'Africa', 'value': 'Africa'},
    #              {'label': 'Americas', 'value': 'Americas'}, {'label': 'Oceania', 'value': 'Oceania'}],
    #     value='All', multi=True),
    dcc.Dropdown(
        id="x-axis-dropdown",
        options=[{'label': cat[1], 'value': cat[0]} for cat in funkt_id_map.items()],
        value='0', multi=False),
    dcc.Dropdown(
        id="y-axis-dropdown",
        options=[{'label': cat[1], 'value': cat[0]} for cat in funkt_id_map.items()],
        value='1', multi=False)
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('x-axis-dropdown', 'value'), Input('y-axis-dropdown', 'value')])
def update_figure(x_axis, y_axis):
    print(x_axis)
    print(y_axis)
    fig = px.scatter(df_ausgaben, x=x_axis, y=y_axis, animation_frame=df_ausgaben.index, animation_group="canton",
                     color="canton", hover_name="canton",
                     log_x=True, size_max=55, range_x=[0.9*df_ausgaben[x_axis].min(), 1.1*df_ausgaben[x_axis].max()],
                     range_y=[0.9*df_ausgaben[y_axis].min(), 1.1*df_ausgaben[y_axis].max()])
    # fig.update_layout(showlegend=False)
    return fig


# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     [Input('year-slider', 'value')])
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#     traces = []
#     for i in filtered_df.continent.unique():
#         df_by_continent = filtered_df[filtered_df['continent'] == i]
#         traces.append(dict(
#             x=df_by_continent['gdpPercap'],
#             y=df_by_continent['lifeExp'],
#             text=df_by_continent['country'],
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 15,
#                 'line': {'width': 0.5, 'color': 'white'}
#             },
#             name=i
#         ))
#
#     return {
#         'data': traces,
#         'layout': dict(
#             xaxis={'type': 'log', 'title': 'GDP Per Capita',
#                    'range': [2.3, 4.8]},
#             yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest',
#             transition={'duration': 1000},
#         )
#     }


# @app.callback(
#     [Output('text-output', 'children'),
#      Output('year-slider', 'value')],
#     [Input('auto-stepper', 'n_intervals'),
#      Input('hidden-div', 'children')])
# def interval_listener(n_intervals, hidden_property):
#     if hidden_property:
#         if n_intervals is None:
#             none_output = 1957
#             return [none_output, none_output]
#         else:
#             not_none_output = n_intervals * 5 + 1957
#             return [not_none_output, not_none_output]
#     return [None, None]

#
# @app.callback(Output('hidden-div', 'children'), [
#     Input('start-button', 'n_clicks')])
# def start_autoplay(n_clicks):
#     if n_clicks:
#         return True
#     else:
#         return False


# ---------------------
# @app.callback(
#     [Output('text-output', 'children'),],
#     [Input('start-button', 'n_clicks'),
#      Input('stop-button', 'n_clicks')])
# def interval_listener(click_start, click_stop):
#     if click_start:
#         for year in df['year'].unique():
#             print(year)
#             update_figure(year)
#             time.sleep(1)
#     return [None]


# ------------------------------

# ----------------------------------
#     Output('play-slider', 'value'), [Input('play-slider', 'n_clicks')])
# def on_click(n_clicks):
#     if n_clicks:
#         print('good')
#     else:
#         print('bad')
#     # for year in df['year'].unique():
#     #     update_figure(str(year))
#     return 'aab'


# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     [Input('auto-stepper', 'n_intervals')])
# def on_click(n_intervals):
#     if n_intervals is None:
#         return 0
#     else:
#         return n_intervals + 1


if __name__ == '__main__':
    app.run_server(debug=True)
