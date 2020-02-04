import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


def get_bubblegraph_tab_layout(min_year, max_year, init_year, year_ticks, funkt_id_map, population_id_map):
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
