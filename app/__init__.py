from flask import Flask

from config import Config

# extensions
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    # configuration
    app.config.from_object(config_class)

    # register extensions
    bootstrap.init_app(app)

    with app.app_context():

        # register blueprints
        from app.main import bp as bp_main
        app.register_blueprint(bp_main)

        from app.dashapps import bp as bp_dashapps
        app.register_blueprint(bp_dashapps)

        # process dash apps

        # dash app 1
        from app.dashapps.dash_app_1 import add_dash as ad1
        app = ad1(app)
        # dash app 2
        from app.dashapps.dash_app_2 import add_dash as ad2
        app = ad2(app)

        return app




