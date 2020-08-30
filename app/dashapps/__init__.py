from flask import Blueprint
import dash_bootstrap_components as dbc
from dash import Dash

bp = Blueprint('dashapps', __name__, template_folder='templates')


from app.dashapps import routes