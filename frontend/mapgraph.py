import dash_core_components as dcc
import dash_html_components as html

def get_map_tab_layout(funkt_id_map):
    return html.Div([
        html.H3('Swiss Cantons'),
        html.Div([
            html.Div([dcc.Graph(id='graph-map', style={'margin': '0 auto', 'display': 'inline-block'}
                                )], style={'width': '70vw', 'text-align': 'center'}),
            html.Div([dcc.Dropdown(
                id='map-value-dropdown',
                options=[{'label': f'{cat[0]} - {cat[1]}', 'value': cat[0]} for cat in funkt_id_map.items()],
                value='0', multi=False, style={'width': '30vw'})]),
        ],
            style={'display': 'flex'}
        ),
    ])