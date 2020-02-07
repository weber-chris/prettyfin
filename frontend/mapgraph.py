import dash_core_components as dcc
import dash_html_components as html


def get_map_tab_layout(funkt_id_map):
    return html.Div([
        html.Div([
            html.Div([html.H3('Swiss Cantons'),
                      dcc.Dropdown(
                          id='map-value-dropdown',
                          options=[{'label': f'{cat[0]} - {cat[1]}', 'value': cat[0]} for cat in funkt_id_map.items()],
                          value='0', multi=False, style={'width': '300px', 'margin': '0px 0px 0px 0px'})],
                     style={'display': 'flex', 'justify-content': 'space-between', 'align-items':'center'}),
            html.Div([
                html.Div([dcc.Graph(id='graph-map', style={'margin': '0 auto', 'width': '97vw', 'height': '63.5vw',
                                                           'max-width': '100vh', 'max-height': '65.5vh',
                                                           'display': 'inline-block'}
                                    )], style={'width': '100%', 'text-align': 'center'}),
            ]),
        ],
            style={'display': 'block'}
        ),
    ])
