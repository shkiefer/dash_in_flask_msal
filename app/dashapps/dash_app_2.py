import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

import numpy as np
import pandas as pd
import plotly.express as px

APP_ID = 'dash_app_2'
URL_BASE = '/dash/dash_app_2/'
MIN_HEIGHT = 600

def add_dash(server):

    FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
    external_stylesheets = [
        FA,
        dbc.themes.BOOTSTRAP,
    ]
    app = dash.Dash(server=server, url_base_pathname=URL_BASE, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
    # make a sample data frame with 6 columns
    np.random.seed(0)
    df = pd.DataFrame({"Col " + str(i + 1): np.random.rand(30) for i in range(6)})

    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='g1', config={'displayModeBar': False}),
                width=4
            ),
            dbc.Col(
                dcc.Graph(id='g2', config={'displayModeBar': False}),
                width=4
            ),
            dbc.Col(
                dcc.Graph(id='g3', config={'displayModeBar': False}),
                width=4
            )
        ])
    ])

    def get_figure(df, x_col, y_col, selectedpoints, selectedpoints_local):

        if selectedpoints_local and selectedpoints_local['range']:
            ranges = selectedpoints_local['range']
            selection_bounds = {'x0': ranges['x'][0], 'x1': ranges['x'][1],
                                'y0': ranges['y'][0], 'y1': ranges['y'][1]}
        else:
            selection_bounds = {'x0': np.min(df[x_col]), 'x1': np.max(df[x_col]),
                                'y0': np.min(df[y_col]), 'y1': np.max(df[y_col])}

        # set which points are selected with the `selectedpoints` property
        # and style those points with the `selected` and `unselected`
        # attribute. see
        # https://medium.com/@plotlygraphs/notes-from-the-latest-plotly-js-release-b035a5b43e21
        # for an explanation
        fig = px.scatter(df, x=df[x_col], y=df[y_col], text=df.index)

        fig.update_traces(selectedpoints=selectedpoints,
                          customdata=df.index,
                          mode='markers+text', marker={'color': 'rgba(0, 116, 217, 0.7)', 'size': 20},
                          unselected={'marker': {'opacity': 0.3}, 'textfont': {'color': 'rgba(0, 0, 0, 0)'}})

        fig.update_layout(margin={'l': 20, 'r': 0, 'b': 15, 't': 5}, dragmode='select', hovermode=False)

        fig.add_shape(dict({'type': 'rect',
                            'line': {'width': 1, 'dash': 'dot', 'color': 'darkgrey'}},
                           **selection_bounds))
        return fig

    # this callback defines 3 figures
    # as a function of the intersection of their 3 selections
    @app.callback(
        [Output('g1', 'figure'),
         Output('g2', 'figure'),
         Output('g3', 'figure')],
        [Input('g1', 'selectedData'),
         Input('g2', 'selectedData'),
         Input('g3', 'selectedData')]
    )
    def callback(selection1, selection2, selection3):
        selectedpoints = df.index
        for selected_data in [selection1, selection2, selection3]:
            if selected_data and selected_data['points']:
                selectedpoints = np.intersect1d(selectedpoints,
                                                [p['customdata'] for p in selected_data['points']])

        return [get_figure(df, "Col 1", "Col 2", selectedpoints, selection1),
                get_figure(df, "Col 3", "Col 4", selectedpoints, selection2),
                get_figure(df, "Col 5", "Col 6", selectedpoints, selection3)]


    return server


if __name__ == '__main__':
    from flask import Flask, render_template
    from flask_bootstrap import Bootstrap

    bootstrap = Bootstrap()
    app = Flask(__name__)
    bootstrap.init_app(app)

    # inject Dash
    app = add_dash(app)

    @app.route(URL_BASE+'debug')
    def dash_app():
        return render_template('dashapps/dash_app_debug.html', dash_url=URL_BASE,
                               min_height=MIN_HEIGHT)

    app_port = 5002
    print(f'http://localhost:{app_port}{URL_BASE}/debug')
    app.run(debug=True, port=app_port)




