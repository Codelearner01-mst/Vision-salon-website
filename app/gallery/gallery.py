from . import main
from flask import render_template


@main.route('/gallery')
def gallery():
    return render_template('gallery.html')
