from app import db

class AppointmentsModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    stylist_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.Integer, nullable=True)
    note = db.Column(db.String(255), nullable=True)

    stylist = db.relationship('TeamModel', backref='bookings')
    service = db.relationship('ServiceModel', backref='bookings')
    user = db.relationship('UserModel', backref='bookings')

    def __init__(self, stylist_id, service_id, total, date=None, note=None):
        self.stylist_id = stylist_id
        self.service_id = service_id
        self.total = total
        self.date = date
        self.time_note = note

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
    
class BookingTimesModel(db.Model):
    __tablename__ = 'time'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(120), nullable=False)

    def __init__(self, time):
        self.time = time

    def json(self):
        return {'id': self.id, 'time': self.time}