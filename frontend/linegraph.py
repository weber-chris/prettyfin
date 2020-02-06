import dash_core_components as dcc
import dash_html_components as html


def get_linegraph_tab_layout(funkt_id_map):
    return html.Div([
        dcc.Graph(id='line-graph', style={'width': '100%', 'height': '65vh'}),
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
                id='y-axis-dropdown',
                options=[{'label': f'{cat[0]} - {cat[1]}', 'value': cat[0]} for cat in funkt_id_map.items()],
                value='1', multi=False, style={'width': '30vw'})]
            )],
            style={'display': 'flex', 'align-items': 'center'})])
