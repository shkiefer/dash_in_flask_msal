import uuid
from flask import redirect, url_for, render_template, flash, current_app, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth import _build_auth_url, _build_msal_app
from app.auth.models import User


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(  # Also logout from your tenant's web session
        current_app.config['AUTHORITY'] + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("main.index", _external=True))


@bp.route('/login', methods=['GET'])
def login():
    next_url = request.args.get('next')
    if not current_user.is_anonymous:
        flash(f'Logged in as {current_user.name}', 'success')
        return redirect(next_url or url_for('main.index'))
    else:
        session["state"] = str(uuid.uuid4())
        auth_url = _build_auth_url(scopes=current_app.config['SCOPE'], state=session["state"])
        return render_template("auth/login.html", auth_url=auth_url)


@bp.route(current_app.config['REDIRECT_PATH'], methods=['GET'])
def authorized():
    next_url = request.args.get('next')

    if request.args.get('state') != session.get("state"):
        return redirect(url_for('main.index'))  # No-OP. Goes back to Index page

    if not current_user.is_anonymous:
        return redirect(next_url or url_for('main.index'))

    if request.args.get('code'):
        result = _build_msal_app().acquire_token_by_authorization_code(
            request.args['code'],
            scopes=current_app.config['SCOPE'],  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("auth.authorized", _external=True))
        if "error" in result:
            flash('Authentication failed', 'danger')
            return redirect(url_for('auth.login'))

        claims = result.get("id_token_claims")
        name = claims['name']
        email = claims['preferred_username']
        if name is None:
            flash('Authentication failed.')
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(name=name).first()

        if not user:
            user = User(name=name, email=email)
            db.session.add(user)
            db.session.commit()

        logged_in = login_user(user, remember=True, force=True)

    else:
        redirect(url_for('auth.login'))

    return redirect(next_url or url_for('main.index'))
