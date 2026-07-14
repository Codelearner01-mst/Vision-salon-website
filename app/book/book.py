from ..models import ServiceModel, TeamModel, BookingTimesModel,AppointmentsModel
from . import main
from flask import render_template,abort,request,jsonify
import datetime as dt
from datetime import date
from app import db



@main.route('/book', methods=["GET","POST"])
def book():
    services = ServiceModel.query.all()
    team_members = TeamModel.query.all()
    booking_times = [bt.json() for bt in BookingTimesModel.query.all()]
    if not services or not team_members or not booking_times:
        abort(404)   
    return render_template('book.html', services=services, team=team_members, booking_times=booking_times)

@main.route('/check-day', methods=["POST"])
def check_day():
    date = request.get_json()
    if date is not None and not isinstance(date["stylist_id"],int) and date["stylist_id"] =="any":
      team_members = TeamModel.query.all()
      for t in team_members:
          if t.day_is_available(date["date"]):
              booked_times = []
              available_appointments_times = AppointmentsModel.query.filter_by(date=date["date"]).all()
              if len(available_appointments_times):
                  for t in available_appointments_times:
                      booked_times.append(t.available_appointment_times_json())
                  return jsonify({"success":"Day is available","booked_times":booked_times})
              return jsonify({"success":"Day is available","booked_times":booked_times})
      return jsonify({"None":"No stylist available on this day."})
    
    if date is not None and isinstance(date["stylist_id"],int):
        member = db.session.get(TeamModel,date["stylist_id"])
        if member is not None:
            if member.day_is_available(date["date"]):
                booked_times = []
                mem_available_appointments_times = AppointmentsModel.query.filter_by(date=date["date"],stylist_id =member.id).all()
                if len(mem_available_appointments_times):
                  for t in mem_available_appointments_times:
                      booked_times.append(t.available_appointment_times_json())
                  return jsonify({"success":"Day is available","booked_times":booked_times})
                return jsonify({"success":"Day is available","booked_times":booked_times})
        return jsonify({"None":"Selected sytlist is not available on this day"})
    return jsonify({"Error":"The request was invalid"})

    
