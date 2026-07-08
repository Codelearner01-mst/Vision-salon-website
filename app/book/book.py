from ..models import ServiceModel, TeamModel, BookingTimesModel
from . import main
from flask import render_template,abort



@main.route('/book')
def book():
    services = ServiceModel.query.all()
    team_members = TeamModel.query.all()
    booking_times = BookingTimesModel.query.all()
    if not services or not team_members or not booking_times:
        abort(404)
    return render_template('book.html', services=services, team=team_members, booking_times=booking_times)
