from flask import Blueprint

bp = Blueprint('dashapps', __name__, template_folder='templates')

from app.dashapps import routes

