from app import db

class TeamModel(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    experience= db.Column(db.String(255), nullable=True)
    info = db.Column(db.String(255), nullable=True)
    stylist = db.Column(db.Boolean, default=False, nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=True)

    specialty = db.relationship('SpecialtiesModel', backref='team_members')

    def __init__(self, image=None, experience=None, info=None, stylist=False, specialty_id=None, role=None):
        self.image = image
        self.experience = experience
        self.info = info
        self.stylist = stylist
        self.specialty_id = specialty_id
        self.role = role

    def json(self):
        return {
            'id': self.id,
            'role': self.role,
            'image': self.image,
            'experience': self.experience,
            'info': self.info,
            'stylist': self.stylist,
            'specialty_id': self.specialty_id,
           
        }


class SpecialtiesModel(db.Model):
    __tablename__ = 'specialties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name}


class TeamSocialsModel(db.Model):
    __tablename__ = 'team_socials'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    social_id = db.Column(db.Integer, db.ForeignKey('socials.id'), nullable=False)
    link = db.Column(db.String(255), nullable=True)

    member = db.relationship('TeamModel', backref='social_links', foreign_keys=[member_id])
    social = db.relationship('SocialModel', backref='team_links')

    def __init__(self, member_id, social_id, link=None):
        self.member_id = member_id
        self.social_id = social_id
        self.link = link

    def json(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'social_id': self.social_id,
            'link': self.link,
        }