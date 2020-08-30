import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dashapps import _protect_dashviews
from app import db
from app.dashapps.models import User_Image

from base64 import b64encode

APP_ID = 'user_image_view'
URL_BASE = '/dash/user_image_view/'
MIN_HEIGHT = 1000

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

    def serve_layout():
        uimgs = db.session.query(User_Image).all()



        return dbc.Container([
            html.H1("View Uploaded Images"),
            html.Div(id=f'{APP_ID}_view_div',
                     children=[
                         dbc.CardDeck([
                             dbc.Card([
                                 dbc.CardImg(src=f"data:image/jpg;base64, {b64encode(uimg.thumb).decode('utf-8')}", top=True, style={"width": "18rem"}),
                                 dbc.CardBody([
                                     html.H4(uimg.name),
                                     html.P(uimg.creator),
                                     dbc.Button('Enlarge', id=f'{APP_ID}_card_button_uimg{uimg.id}', color='primary')
                                 ]),
                                 dbc.CardFooter(
                                     dbc.CardLink('Web Link', href=f'{uimg.img_web_url}',
                                                  external_link=True, target="_blank")
                                 )
                             ],
                                 style={"max-width": "18rem"},
                             ) for uimg in uimgs
                         ],
                         )
                     ]
                     ),
            # todo add modal display
        ])

    app.layout = serve_layout

    if login_reg:
        _protect_dashviews(app)

    return server


if __name__ == '__main__':
    from flask import Flask, render_template
    from flask_bootstrap import Bootstrap
    from flask_sqlalchemy import SQLAlchemy
    from config import Config
    from app import create_app

    bootstrap = Bootstrap()
    Config.TESTING = True
    app = Flask(__name__)
    # configuration
    app.config.from_object(Config)

    # register extensions
    db.init_app(app)
    bootstrap.init_app(app)

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

    # inject Dash
    app = add_dash(app, login_reg=False)

    @app.route(URL_BASE+'debug')
    def dash_app():
        return render_template('dashapps/dash_app_debug.html', dash_url=URL_BASE,
                               min_height=MIN_HEIGHT)

    app_port = 5002
    print(f'http://localhost:{app_port}{URL_BASE}debug')
    app.run(debug=True, port=app_port)
