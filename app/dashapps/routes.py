from flask import render_template

from app.dashapps import bp
from app.dashapps import dash_app_1 as dash_app_1_obj
from app.dashapps import dash_app_2 as dash_app_2_obj


@bp.route("/dash_app_1")
def dash_app_1():
    return render_template('dashapps/dash_app.html', dash_url=dash_app_1_obj.URL_BASE, min_height=dash_app_1_obj.MIN_HEIGHT)


@bp.route("/dash_app_2")
def dash_app_2():
    return render_template('dashapps/dash_app.html', dash_url=dash_app_2_obj.URL_BASE, min_height=dash_app_2_obj.MIN_HEIGHT)




