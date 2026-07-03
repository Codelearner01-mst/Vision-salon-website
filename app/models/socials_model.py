from app import db

class SocialModel(db.Model):
    __tablename__ = 'socials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name}