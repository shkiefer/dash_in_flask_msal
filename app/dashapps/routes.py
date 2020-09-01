from flask import render_template
from flask_login import login_required

from app.dashapps import bp
from app.dashapps import dash_app_1 as dash_app_1_obj
from app.dashapps import dash_app_2 as dash_app_2_obj
from app.dashapps import user_image_upload as user_image_upload_obj
from app.dashapps import user_image_view as user_image_view_obj

@bp.route("/dash_app_1")
@login_required
def dash_app_1():
    return render_template('dashapps/dash_app.html', dash_url=dash_app_1_obj.URL_BASE, min_height=dash_app_1_obj.MIN_HEIGHT)


@bp.route("/dash_app_2")
def dash_app_2():
    return render_template('dashapps/dash_app.html', dash_url=dash_app_2_obj.URL_BASE, min_height=dash_app_2_obj.MIN_HEIGHT)


@bp.route('/image_view')
def user_image_view():
    return render_template('dashapps/dash_app.html', dash_url=user_image_view_obj.URL_BASE,
                           min_height=user_image_view_obj.MIN_HEIGHT)

@bp.route('/image_upload')
@login_required
def user_image_upload():
    return render_template('dashapps/dash_app.html', dash_url=user_image_upload_obj.URL_BASE,
                           min_height=user_image_upload_obj.MIN_HEIGHT)

