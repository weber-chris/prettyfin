import dash_core_components as dcc
import dash_html_components as html


def get_linegraph_tab_layout(funkt_id_map, disabled_cat_ausgaben):
    return html.Div([
        dcc.Graph(id='line-graph', style={'min-width': '50vh', 'height': '65vh', 'flex': '1 0 auto'}),
        html.Div([
            html.Div([dcc.RadioItems(
                id='normalize-radio',
                options=[
                    {'label': 'Absolute', 'value': 'absolute'},
                    {'label': 'Normalized', 'value': 'normalized'}
                ],
                value='absolute'
            )], style={}),
            html.Div([dcc.Dropdown(
                id='y-axis-dropdown',
                options=[{'label': f'{cat[0]} - {cat[1]}', 'value': cat[0], 'disabled': cat[0] in disabled_cat_ausgaben}
                         for cat in funkt_id_map.items()],
                value='1', multi=False, style={})]
            )], style={'width': 250, 'flex': '1 0 auto', 'margin': '20px 20px 0px 0px'})],
        style={'display': 'flex', 'flex-wrap': 'wrap', 'width': '98vw'})
