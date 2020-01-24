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


if __name__ == '__main__':
    app.run_server(debug=True)
