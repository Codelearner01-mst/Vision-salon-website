from . import main
from flask import render_template


@main.route('/contact')
def contact():
    return render_template('contact.html')
