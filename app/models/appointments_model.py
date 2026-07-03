from app import db

class AppointmentsModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    stylist_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(255), nullable=True)

    def __init__(self, stylist_id, service_id, total, date=None, notes=None):
        self.stylist_id = stylist_id
        self.service_id = service_id
        self.total = total
        self.date = date
        self.notes = notes

    def json(self):
        return {
            'id': self.id,
            'stylist_id': self.stylist_id,
            'service_id': self.service_id,
            'total': self.total,
            'date': self.date,
            'notes': self.notes,
        }