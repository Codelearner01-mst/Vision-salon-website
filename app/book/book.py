from app.models.team_model import TeamModel
from app.models.service_model import ServiceModel
from . import main
from flask import render_template,abort



@main.route('/book')
def book():
    services = ServiceModel.query.all()
    team_members = TeamModel.query.all()
    if not services or not team_members:
        abort(404)
    return render_template('book.html', services=services, team=team_members)
