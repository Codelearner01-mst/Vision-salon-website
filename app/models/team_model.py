from app import db
import datetime 
from datetime import date

class TeamModel(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    years_of_experience = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.String(400), nullable=True)
    about = db.Column(db.Text, nullable=True)
    stylist = db.Column(db.Boolean, default=False, nullable=False)

    workdays = db.relationship('WeekdaysModel', secondary='team_workdays', backref='team_members', overlaps='workday_links')

    def __init__(self, name, image=None, years_of_experience=None, bio=None, about=None, stylist=False, role=None):
        self.name = name
        self.image = image
        self.years_of_experience = years_of_experience
        self.bio = bio
        self.about = about
        self.stylist = stylist
        self.role = role

    def day_is_available(self,date):
       if not date or date is None:
        return False
       date = date.split("-")
       year, month, day= [int(date[0]),int(date[1]),int(date[2])]
       day_num = datetime.date(year,month,day).weekday()
       workdays = self.workdays
       for wd in workdays:
         if day_num == wd.day_num:
           return True
       return False

    def json(self):
        return {
            'id': self.id,
            "name": self.name,
            'role': self.role,
            'image': self.image,
            'years_of_experience': self.years_of_experience,
            'bio': self.bio,
            'about': self.about,
            'stylist': self.stylist,
            "specialties": [s.name for s in self.specialties],
             "workdays":[d.name for d in self.workdays]
           
        }


class SpecialtiesModel(db.Model):
    __tablename__ = 'specialties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    member = db.relationship('TeamModel', backref='specialties')

    def __init__(self, name,member_id):
        self.name = name
        self.member_id = member_id

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

class WeekdaysModel(db.Model):
    __tablename__ = 'weekdays'

    id = db.Column(db.Integer, primary_key=True)
    day_num = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, day_num, name):
        self.day_num = day_num
        self.name = name

    def json(self):
        return {'id': self.id, 'day_num': self.day_num, 'name': self.name}


class TeamWorkdaysModel(db.Model):
    __tablename__ = 'team_workdays'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('weekdays.id'), nullable=False)

    member = db.relationship('TeamModel', overlaps='workdays,team_members')
    day = db.relationship('WeekdaysModel', overlaps='workdays,team_members')

    def __init__(self, member_id, day_id):
        self.member_id = member_id
        self.day_id = day_id

    def json(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'day_id': self.day_id,
        }
