from ..models import ServiceModel, TeamModel, BookingTimesModel,AppointmentsModel
from . import main
from flask import render_template,abort,request,jsonify,current_app
import datetime as dt
from datetime import date
from app import db
from app.email import send_email 


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

@main.route('/book-appointment', methods=["POST"])
def book_appointment():
    book_details = request.get_json()
    if not book_details or book_details is None:
        return jsonify({"invalid":"Couldn't placed the order. Got invalid details!"})
    if not book_details["guest_details"]:
        return jsonify({"invalid":"Couldn't placed the order. Quest details was not provided!"})
    try:
        service_id, stylist_id, total,booking_date,time_id = [book_details["service_id"],book_details["stylist_id"],book_details["total"],book_details["date"],book_details["time_id"]]
        # Convert date string to Python date object for SQLite
        if isinstance(booking_date, str):
            booking_date = dt.datetime.strptime(booking_date, "%Y-%m-%d").date()
        guest = book_details["guest_details"]
        name, email, note, phone = [guest["guest_name"],guest["email"],guest["note"],guest["phone_number"]]
        appointment = AppointmentsModel(stylist_id,service_id,total,booking_date,time_id,name,email,phone,note)
        db.session.add(appointment)
        db.session.commit()
        successMsg = f'Thank you, {name} Your appointment for {appointment.service.name} with {appointment.stylist.name} on {appointment.date} at {appointment.appointment_time.time.strftime("%H:%M:%S")} has been successfully requested. We will email confirmation details to you.'
        send_email(
            to=appointment.email,
            subject="Booking Confirmation - Vision Salon",
            template="email/booking_success_email",
            sender=current_app.config['VISION_MAIL_SENDER'],
            name=name,
            service_name=appointment.service.name,
            stylist_name=appointment.stylist.name,
            date=appointment.date,
            time=appointment.appointment_time.time.strftime("%I:%M %p"),
            total=appointment.total,
            note=appointment.note,
            phone_number=appointment.phone_number
        )
        return jsonify({"success":successMsg})
    except Exception as e:
        db.session.rollback()
        print("Exception error",e)
        return jsonify({"error":"Oops.Error occured while placing order. Try again later!"})