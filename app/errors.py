from .main import main
from flask import render_template

@main.app_errorhandler(404)
def error404(e):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def error500(e):
    return render_template('errors/500.html'), 500