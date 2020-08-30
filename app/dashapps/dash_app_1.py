import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

APP_ID = 'dash_app_1'
URL_BASE = '/dash/dash_app_1/'
MIN_HEIGHT = 200

def add_dash(server, login_reg=True):

    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
    ]

    app = dash.Dash(
        server=server,
        url_base_pathname=URL_BASE,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets
    )

    app.layout = dbc.Container([
        html.H6("Change the value in the text box to see callbacks in action!"),
        html.Div(["Input: ",
                  dcc.Input(id=f'{APP_ID}_my_input', value='initial value', type='text')]),
        html.Br(),
        html.Div(id=f'{APP_ID}_my_output'),

    ])

    @app.callback(
        Output(component_id=f'{APP_ID}_my_output', component_property='children'),
        [Input(component_id=f'{APP_ID}_my_input', component_property='value')]
    )
    def update_output_div(input_value):
        return 'Output: {}'.format(input_value)


    return server


if __name__ == '__main__':
    from flask import Flask, render_template
    from flask_bootstrap import Bootstrap

    bootstrap = Bootstrap()
    app = Flask(__name__)
    bootstrap.init_app(app)

    # inject Dash
    app = add_dash(app, login_reg=False)

    @app.route(URL_BASE+'debug')
    def dash_app():
        return render_template('dashapps/dash_app_debug.html', dash_url=URL_BASE,
                               min_height=MIN_HEIGHT)

    app_port = 5001
    print(f'http://localhost:{app_port}{URL_BASE}/debug')
    app.run(debug=True, port=app_port)
