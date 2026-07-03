from app import db

class AppointmentsModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    stylist_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.Integer, nullable=True)
    time_note = db.Column(db.String(255), nullable=True)

    stylist = db.relationship('TeamModel', backref='bookings')
    service = db.relationship('ServiceModel', backref='bookings')

    def __init__(self, stylist_id, service_id, total, date=None, time_note=None):
        self.stylist_id = stylist_id
        self.service_id = service_id
        self.total = total
        self.date = date
        self.time_note = time_note

    def json(self):
        return {
            'id': self.id,
            'stylist_id': self.stylist_id,
            'service_id': self.service_id,
            'total': self.total,
            'date': self.date,
            'time_note': self.time_note,
        }