from app import db

class ServiceModel(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    headline = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    duration_min = db.Column(db.Integer, nullable=False)
    duration_max = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)
    descriptionII = db.Column(db.String(250), nullable=True)

    def __init__(self, headline, name,description, image, duration_min, duration_max, price=None, descriptionII=None):
        self.headline = headline
        self.name = name
        self.description = description
        self.image = image
        self.duration_min = duration_min
        self.duration_max = duration_max
        self.price = price
        self.descriptionII = descriptionII

    def json(self,service_includes=""):
        return {
            'id': self.id,
            'headline': self.headline,
            "name":self.name,
            'description': self.description,
            'image': self.image,
            'duration_min': self.duration_min,
            'duration_max': self.duration_max,
            'price': self.price,
            'descriptionII': self.descriptionII,
            "sub_works": [],
            "service_includes":[s.name for s in service_includes]
        }

class SubServiceModel(db.Model):
    __tablename__ = 'sub_services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)

    service = db.relationship('ServiceModel', backref='sub_services')

    def __init__(self, name,service_id):
        self.name = name
        self.service_id = service_id

    def json(self):
        return {'id': self.id, 'name': self.name,"service_id":self.service_id}


class ServiceIncludesModel(db.Model):
    __tablename__ = 'service_includes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    service_id =  db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)

    service = db.relationship('ServiceModel', backref='service_includes')

    def __init__(self, name,service_id):
        self.name = name
        self.service_id = service_id

    def json(self):
        return {'id': self.id, 'name': self.name,"service_id":self.service_id}