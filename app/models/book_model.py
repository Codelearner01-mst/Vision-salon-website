from app import db
from datetime import time
from sqlalchemy import UniqueConstraint

class AppointmentsModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    stylist_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_id = db.Column(db.Integer,db.ForeignKey('time.id'),nullable=False)
    note = db.Column(db.String(255), nullable=True)
    quest_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(30), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "date", "time_id", "stylist_id",
            name="uq_booked_slot"
        ),
    )

    stylist = db.relationship('TeamModel', backref='bookings')
    service = db.relationship('ServiceModel', backref='bookings')
    user = db.relationship('UserModel', backref='bookings')
    appointment_time = db.relationship("BookingTimesModel",backref="bookings")

    def __init__(self, stylist_id, service_id, total, date, time_id,  quest_name, email ,  phone_number,note=None):
        self.stylist_id = stylist_id
        self.service_id = service_id
        self.total = total
        self.date = date
        self.time_id = time_id
        self.note = note
        self.quest_name = quest_name
        self.email = email 
        self.phone_number = phone_number

    def json(self):
        return {
            'id': self.id,
            'stylist_id': self.stylist_id,
            'service_id': self.service_id,
            "user_id": self.user_id,
            'total': self.total,
            'date': self.date,
            'time_note': self.note,
        }
    def available_appointment_times_json(self):
        return {
            'id': self.appointment_time.id,
            "time":self.appointment_time.time.strftime("%H:%M:%S")
        }
    
class BookingTimesModel(db.Model):
    __tablename__ = 'time'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=False)

    def __init__(self, time):
        self.time = time

    def json(self):
        return {'id': self.id, 'time': self.time.strftime('%I:%M %p') if self.time else None}