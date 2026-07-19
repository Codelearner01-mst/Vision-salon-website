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

    # Use .get() to safely check for missing keys
    service_id = book_details.get("service_id")
    stylist_id = book_details.get("stylist_id")
    total = book_details.get("total")
    booking_date = book_details.get("date")
    time_id = book_details.get("time_id")
    guest = book_details.get("guest_details")

    if not service_id:
        return jsonify({"invalid":"Service was not selected. Please select a service."})
    if not stylist_id and stylist_id != 0:
        return jsonify({"invalid":"Stylist was not selected. Please select a stylist."})
    if not total and total != 0:
        return jsonify({"invalid":"Total price is missing."})
    if not booking_date:
        return jsonify({"invalid":"Date was not selected. Please select a date."})
    if not time_id:
        return jsonify({"invalid":"Time slot was not selected. Please select a time."})
    if not guest:
        return jsonify({"invalid":"Couldn't placed the order. Quest details was not provided!"})

    # Validate guest_details keys
    name = guest.get("guest_name")
    email = guest.get("email")
    phone = guest.get("phone_number")
    note = guest.get("note", "")
    if not name:
        return jsonify({"invalid":"Your name is required."})
    if not email:
        return jsonify({"invalid":"Your email is required."})
    if not phone:
        return jsonify({"invalid":"Your phone number is required."})

    # Verify service_id and stylist_id exist in the database
    service = db.session.get(ServiceModel, service_id)
    if service is None:
        return jsonify({"invalid":"The selected service does not exist."})
    if isinstance(stylist_id, int):
        stylist = db.session.get(TeamModel, stylist_id)
        if stylist is None:
            return jsonify({"invalid":"The selected stylist does not exist."})

    try:
        # Convert date string to Python date object for SQLite
        if isinstance(booking_date, str):
            booking_date = dt.datetime.strptime(booking_date, "%Y-%m-%d").date()
        if not isinstance(stylist_id,int) and (stylist_id == "Any" or stylist_id == "Any".lower()):
            booked = db.session.query(AppointmentsModel.stylist_id).filter(AppointmentsModel.time_id == time_id, AppointmentsModel.date == booking_date) 
            available  = TeamModel.query.filter(~TeamModel.id.in_(booked)).all()
            if len(available) == 1:
                 stylist_id = available[0].id
                 appointment = AppointmentsModel(stylist_id,service_id,total,booking_date,time_id,name,email,phone,note)
            else:
                import random
                random_stylist = random.choice([stylist for stylist in available])
                stylist_id = random_stylist.id
                appointment = AppointmentsModel(stylist_id,service_id,total,booking_date,time_id,name,email,phone,note)
            db.session.add(appointment)
            db.session.commit()
            successMsg = f'Thank you, {name} Your appointment for {appointment.service.name} with any stylist available on {appointment.date} at {appointment.appointment_time.time.strftime("%I:%M %p")} has been successfully requested. We will email confirmation details to you.'
            send_email(
            to=appointment.email,
            subject="Booking Confirmation - Vision Salon",
            template="email/booking_success_email",
            sender=current_app.config['VISION_MAIL_SENDER'],
            name=name,
            service_name=appointment.service.name,
            stylist_name= "Any available stylist",
            date=appointment.date,
            time=appointment.appointment_time.time.strftime("%I:%M %p"),
            total=appointment.total,
            note=appointment.note,
            phone_number=appointment.phone_number
        )
            return jsonify({"success":successMsg})
        
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