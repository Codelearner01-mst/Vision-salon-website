from . import main
from flask import render_template


@main.route('/story')
def story():
    return render_template('story.html')
