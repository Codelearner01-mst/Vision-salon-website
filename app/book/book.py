from . import main
from flask import render_template
from ..service.service_data import services_data
from ..team.team_data import team_data


@main.route('/book')
def book():
    return render_template('book.html', services=services_data.values(), team=team_data.values())
