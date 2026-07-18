from ..models import ServiceModel, TeamModel, BookingTimesModel,AppointmentsModel,WeekdaysModel,TeamWorkdaysModel
from . import main
from flask import render_template,abort,request,jsonify,current_app
import datetime as dt
from app import db
from app.email import send_email 
from app.helper.date import get_day_num
from sqlalchemy.exc import IntegrityError


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
      day_num = get_day_num(date["date"])
      available_stylists = TeamModel.query.filter(TeamModel.workdays.any(WeekdaysModel.day_num == day_num)).all()
      day_is_available = TeamWorkdaysModel.query.filter(TeamWorkdaysModel.day.has(WeekdaysModel.day_num==day_num)).all()
      if day_is_available:
          booked_times = []
          appointments = AppointmentsModel.query.filter_by(date=date["date"]).all()
          if len(appointments):
              times = [a.appointment_time for a in appointments]
              for t in times:
                  if t in booked_times:
                     continue
                  if times.count(t)==len(available_stylists):
                     booked_times.append(t)
              booked_times = [bt.json() for bt in booked_times]
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
        successMsg = f'Thank you, {name} Your appointment for {appointment.service.name} with {appointment.stylist.name} on {appointment.date} at {appointment.appointment_time.time.strftime("%I:%M %p")} has been successfully requested. We will email confirmation details to you.'
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
    except IntegrityError as e:
        db.session.rollback()
        print("Exception error",e)
        
        # 1. Convert the raw Postgres error to a string
    # It looks like: "...violates unique constraint 'uq_booked_slot'..."
        error_message = str(e.orig)
    
    # 2. Check for your exact unique constraint name
        if "uq_booked_slot" in error_message:
           return jsonify({
            "status": "error", 
            "code": "SLOT_TAKEN",
            "message": "Sorry, this time slot was just booked by another user."
           }), 409  # 409 Conflict is the standard HTTP status code for this

       # 3. Check for other potential issues (like a deleted/missing user ID)
        elif "foreign key" in error_message:
           return jsonify({
            "status": "error",
            "code": "INVALID_USER",
            "message": "Booking failed. The associated user account does not exist."
          }), 400

    # 4. Fallback for any other unexpected database constraint failures
        else:
           return jsonify({
            "status": "error", 
            "code": "DATABASE_ERROR",
            "message": "An unexpected system error occurred. Please try again."
        }), 500

    finally:
     db.session.close()