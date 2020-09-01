from flask import Blueprint
import uuid
from flask import url_for, current_app
import msal

bp = Blueprint('auth', __name__, template_folder='templates')


def _build_msal_app(authority=None):
    return msal.ConfidentialClientApplication(
        current_app.config['CLIENT_ID'], authority=authority or current_app.config['AUTHORITY'],
        client_credential=current_app.config['CLIENT_SECRET'])


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("auth.authorized", _external=True))


from app.auth import routes