from flask import Flask, render_template, session, request, redirect, url_for
import msal

from app.main import bp

@bp.route("/")
@bp.route("/index")
def index():
    return render_template('index.html')
