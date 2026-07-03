from app import db

class ServiceModel(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    duration_min = db.Column(db.Integer, nullable=False)
    duration_max = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)
    descriptionII = db.Column(db.String(200), nullable=True)
    sub_service_id = db.Column(db.Integer, db.ForeignKey('sub_services.id'), nullable=True)
    service_includes_id = db.Column(db.Integer, db.ForeignKey('service_includes.id'), nullable=True)

    sub_service = db.relationship('SubServiceModel', backref='services')
    service_include = db.relationship('ServiceIncludesModel', backref='services')

    def __init__(self, headline, description, image, duration_min, duration_max, price=None, descriptionII=None, sub_service_id=None, service_includes_id=None):
        self.headline = headline
        self.description = description
        self.image = image
        self.duration_min = duration_min
        self.duration_max = duration_max
        self.price = price
        self.descriptionII = descriptionII
        self.sub_service_id = sub_service_id
        self.service_includes_id = service_includes_id

    def json(self):
        return {
            'id': self.id,
            'headline': self.headline,
            'description': self.description,
            'image': self.image,
            'duration_min': self.duration_min,
            'duration_max': self.duration_max,
            'price': self.price,
            'descriptionII': self.descriptionII,
            'sub_service_id': self.sub_service_id,
            'service_includes_id': self.service_includes_id,
        }


class SubServiceModel(db.Model):
    __tablename__ = 'sub_services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name}


class ServiceIncludesModel(db.Model):
    __tablename__ = 'service_includes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name}