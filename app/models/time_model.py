from app import db

class TimeModel(db.Model):
    __tablename__ = 'time'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(120), nullable=False)

    def __init__(self, time):
        self.time = time

    def json(self):
        return {'id': self.id, 'time': self.time}