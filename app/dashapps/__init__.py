from flask import Blueprint
import dash_bootstrap_components as dbc
from dash import Dash
from flask_login import login_required

bp = Blueprint('dashapps', __name__, template_folder='templates')

def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


from app.dashapps import routes