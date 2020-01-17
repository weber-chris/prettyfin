import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import time

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Interval(id='auto-stepper',
                 interval=5 * 1000,  # in milliseconds
                 n_intervals=0
                 ),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        updatemode='drag',
        step=None
    ),
    html.Div('bla', id='text-output'),
    html.Button('Start', id='start-button'),
    html.Button('Stop', id='stop-button'),
    html.Div(id='hidden-div', style={'display': 'none'})
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(dict(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'log', 'title': 'GDP Per Capita',
                   'range': [2.3, 4.8]},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition={'duration': 1000},
        )
    }


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
