from flask import Flask
from config import Config
# extensions
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
lm = LoginManager()
lm.login_view = 'auth.login'
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    # configuration
    app.config.from_object(config_class)

    # register extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    lm.init_app(app)

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

    with app.app_context():
        # register blueprints
        from app.main import bp as bp_main
        app.register_blueprint(bp_main)
        from app.auth import bp as bp_auth
        app.register_blueprint(bp_auth, url_prefix='/auth')
        from app.dashapps import bp as bp_dashapps
        app.register_blueprint(bp_dashapps)

        # process dash apps
        # dash app 1
        from app.dashapps.dash_app_1 import add_dash as ad1
        app = ad1(app, login_reg=False)
        # dash app 2
        from app.dashapps.dash_app_2 import add_dash as ad2
        app = ad2(app, login_reg=False)
        # dash user image upload
        from app.dashapps.user_image_upload import add_dash as ad3
        app = ad3(app, login_reg=True)
        # dash user image view
        from app.dashapps.user_image_view import add_dash as ad4
        app = ad4(app, login_reg=False)

        return app


