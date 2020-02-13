import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from pathlib import Path
import os
import json
import pandas as pd
import frontend.bubblegraph
import frontend.linegraph
import frontend.mapgraph
import numpy as np
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
with open(folder_preprocessed_data / 'canton_borders.json', 'r') as file:
    canton_borders = json.load(file)
with open(folder_preprocessed_data / 'canton_borders_xy.json', 'r') as file:
    canton_borders_xy = json.load(file)
disabled_cat_ausgaben = ['03', '08', '13', '18', '26', '27', '28', '38', '48', '58', '64', '68', '76', '78', '86', '88',
                         '91', '92', '93', '94', '95', '97', '99']

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

app.title = 'PrettyFin'


def year_tick_formater(year_ticks):
    slider_ticks = {}
    for year in year_ticks:
        if int(year) % 2 == 0:
            slider_ticks[year] = ''
        else:
            slider_ticks[year] = year
    return slider_ticks


app.layout = html.Div([
    html.H1('Prettyfin'),
    dcc.Tabs(id="tabs", value='tab-map', children=[
        dcc.Tab(label='Bubble Graph', value='tab-graph'),
        dcc.Tab(label='Line Graph', value='tab-line'),
        dcc.Tab(label='Map', value='tab-map')
    ]),
    html.Div(id='tabs-content'),
    html.Div([
        html.Div(
            [html.Button(html.P('Play', id='start-button-text', style={}), id='start-button')],
            style={}),
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=min_year,
                max=max_year,
                value=init_year,
                marks=year_tick_formater(year_ticks),
                # marks=year_ticks,
                updatemode='drag',
                step=None
            )], style={'width': '100%', 'margin': '5px 0px 0px 0px'})],
        style={'align-content': 'stretch'}, id='timeline-div'),
    dcc.Interval(id='interval', disabled=True, interval=1200),
])


@app.callback([Output('tabs-content', 'children'), Output('timeline-div', 'style')],
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-graph':
        return frontend.bubblegraph.get_bubblegraph_tab_layout(funkt_id_map, disabled_cat_ausgaben,
                                                               population_id_map), {'display': 'flex'}
    elif tab == 'tab-line':
        return frontend.linegraph.get_linegraph_tab_layout(funkt_id_map, disabled_cat_ausgaben), {'display': 'none'}
    elif tab == 'tab-map':
        return frontend.mapgraph.get_map_tab_layout(funkt_id_map, disabled_cat_ausgaben), {'display': 'flex'}


@app.callback(Output('start-button-text', 'children'), [Input('interval', 'disabled')])
def change_button_text(disabled):
    if disabled:
        return 'Play'
    else:
        return 'Stop'


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
     Input('normalize-checkbox-bubble', 'value'),
     Input('year-slider', 'value')]
)
def update_bubble(x_axis, y_axis, bubble_size_dropdown, normalize, selected_year):
    print('update_bubble')

    df_filtered = df_ausgaben[df_ausgaben.year == selected_year]
    traces = []
    for canton in cantons:
        df_canton = df_filtered[df_filtered['canton'] == canton]

        if normalize == ['normalized']:
            x_vals = min_max_normalization_one_canton_all_cat(df_canton, df_ausgaben, x_axis, canton)
            y_vals = min_max_normalization_one_canton_all_cat(df_canton, df_ausgaben, y_axis, canton)
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

    # factor to show some margin, because bubbles span over the edges
    extra_space_graph = 0.05
    if normalize == ['normalized']:
        x_range = [-extra_space_graph, 1 + extra_space_graph]
        y_range = [-extra_space_graph, 1 + extra_space_graph]
    else:
        x_range = [
            df_ausgaben[x_axis].min() - extra_space_graph * (df_ausgaben[x_axis].max() - df_ausgaben[x_axis].min()),
            df_ausgaben[x_axis].max() + extra_space_graph * (df_ausgaben[x_axis].max() - df_ausgaben[x_axis].min())]
        y_range = [
            df_ausgaben[y_axis].min() - extra_space_graph * (df_ausgaben[y_axis].max() - df_ausgaben[y_axis].min()),
            df_ausgaben[y_axis].max() + extra_space_graph * (df_ausgaben[y_axis].max() - df_ausgaben[y_axis].min())]
        # x_range = [df_ausgaben[x_axis].min(), df_ausgaben[x_axis].max()]
        # y_range = [df_ausgaben[y_axis].min(), df_ausgaben[y_axis].max()]
    fig = {
        'data': traces,
        'layout': dict(
            xaxis={'title': {'text': funkt_id_map[x_axis], 'font': {'size': 16}, 'standoff': 5},
                   'range': x_range, 'fixedrange': True},
            yaxis={'title': {'text': funkt_id_map[y_axis], 'font': {'size': 16}},
                   'range': y_range, 'fixedrange': True},
            margin={'l': 60, 'b': 200, 't': 10, 'r': 20},
            legend={'y': 0, 'orientation': 'h', 'yanchor': 'top', 'borderwidth': 35, 'bordercolor': '#00000000',
                    'font': {'size': 13}},
            # legend={'x': 1, 'y': 1, 'font': {'size': 13}},
            hovermode='closest',
            transition={'duration': 1000},
        )}

    return fig


@app.callback(
    Output('line-graph', 'figure'),
    [Input('y-axis-dropdown', 'value'),
     Input('normalize-checkbox-line', 'value')]
)
def update_line(y_axis, normalize):
    print('update_line')

    traces = []
    for canton in cantons:
        df_canton = df_ausgaben[df_ausgaben['canton'] == canton]

        if normalize == ['normalized']:
            y_vals = min_max_normalization_one_canton_all_cat(df_canton, df_ausgaben, y_axis, canton)
        else:
            y_vals = df_canton[y_axis]

        traces.append(dict(
            x=df_canton['year'],
            y=y_vals,
            # x=df_canton[x_axis],
            # y=df_canton[y_axis],
            text=df_canton['canton'].apply(lambda x: iso_canton_map[x]),
            mode='lines+markers',
            opacity=0.7,
            marker={
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=iso_canton_map[canton]
        ))
    if normalize == ['normalized']:
        y_range = [0, 1]
    else:
        y_range = [df_ausgaben[y_axis].min(), df_ausgaben[y_axis].max()]
    fig = {
        'data': traces,
        'layout': dict(
            xaxis={'fixedrange': True},
            yaxis={'title': {'text': funkt_id_map[y_axis], 'font': {'size': 16}},
                   'range': y_range, 'fixedrange': True},
            margin={'l': 60, 'b': 200, 't': 10, 'r': 20},
            legend={'y': 0, 'orientation': 'h', 'yanchor': 'top', 'borderwidth': 35, 'bordercolor': '#00000000',
                    'font': {'size': 13}},
            # legend={'x': 1, 'y': 1, 'font': {'size': 13}},
            hovermode='closest',
            transition={'duration': 1000},
        )}

    return fig


@app.callback(
    Output('graph-map', 'figure'),
    [Input('map-value-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('normalize-checkbox-map', 'value')
     ])
def update_map(category, year, normalized):
    fig = go.Figure()

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=0), showlegend=False)
    # Update axes properties
    fig.update_xaxes(
        range=[35, 1050],  # 85
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        fixedrange=True
    )

    fig.update_yaxes(
        range=[665, 0],
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        fixedrange=True
    )

    canton_shapes = []

    df_filtered = df_ausgaben[df_ausgaben.year == year]
    for canton in cantons:
        # display_value = df_filtered[df_filtered['canton'] == 'ag'][category].values[0]
        df_canton = df_filtered[df_filtered['canton'] == canton]
        display_value = df_canton[category].values[0]
        display_value_normalized_canton = min_max_normalization_all_canton_one_cat(df_canton, df_ausgaben, category)
        display_value_normalized_ch = min_max_normalization_one_canton_all_cat(df_canton, df_ausgaben, category, canton)

        if normalized:
            display_color = value_to_heat_color(display_value_normalized_ch)
            display_value_normalized = display_value_normalized_ch
        else:
            display_color = value_to_heat_color(display_value_normalized_canton)
            display_value_normalized = display_value_normalized_canton

        canton_shape = canton_borders[canton.upper()]
        canton_shapes.append(go.layout.Shape(type='path', path=canton_shape, fillcolor=display_color,
                                             line_color="LightSeaGreen"))

        for subarea in canton_borders_xy[canton.upper()]:
            fig.add_trace(
                go.Scatter(
                    x=subarea[0],
                    y=subarea[1],
                    text=f'<span style="font-size:20;font-weight:bold;">{iso_canton_map[canton]}</span><br />'
                         + f'CHF {display_value:,.{0}f}<br />'
                         + f'{display_value_normalized.values[0] * 100:.{2}f}%</span>',
                    hoverinfo="text",
                    hoveron="fills",
                    fill="toself",
                    fillcolor="LightSeaGreen",
                    opacity=0

                ))
    # Add shapes
    fig.update_layout(shapes=canton_shapes)

    fig.add_trace(
        go.Scatter(
            x=[0, 0],
            y=[1, 1],
            opacity=0,
            marker=dict(size=16, colorscale=[[0, 'rgb(255,0,0)'], [1, 'rgb(0,0,255)']],
                        showscale=True, cmax=1, cmin=0)
            # marker=dict(size=16, colorscale='Bluered',
            #             showscale=True)

        ))
    return fig


def min_max_normalization_one_canton_all_cat(df_canton_year, df_all, axis, canton):
    """
    Normalize the value to [0:1] in correspondence to the specific canton's min / max over all categories
    """
    df_canton_all = df_all[df_all['canton'] == canton][axis]
    x = (df_canton_year[axis] - df_canton_all.min()) / (df_canton_all.max() - df_canton_all.min())
    return x


def min_max_normalization_one_canton_one_cat(df_canton_year, df_all, category, canton):
    """
    Normalize the value to [0:1] in correspondence to the specific canton's min / max over specify category
    """
    df_canton_all = df_all[df_all['canton'] == canton][category]
    x = (df_canton_year[category] - df_canton_all[category].min()) / (
            df_canton_all[category].max() - df_canton_all[category].min())
    return x


def min_max_normalization_all_canton_one_cat(df_canton_year, df_all, category):
    """
    Normalize the value to [0:1] in correspondence to min / max in this category over all cantons
    """
    x = (df_canton_year[category] - df_all[category].min()) / (df_all[category].max() - df_all[category].min())
    return x


def value_to_heat_color(value):
    val = value.values[0]
    if np.isnan(val):
        return 'rgb(0,0,0)'
    else:
        b = 255 * (1 - val)
        r = 255 * val
        return f'rgb({round(r):.{0}f},{0},{round(b):.{0}f})'


if __name__ == '__main__':
    app.run_server(debug=True)
