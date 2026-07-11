import unittest
from app import create_app, db
from app.models import BookingTimesModel, ServiceModel, TeamModel
from app.models.team_model import WeekdaysModel, TeamWorkdaysModel
from datetime import time


class TestBook(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        bt = BookingTimesModel(time=time(10, 0))
        bt2 = BookingTimesModel(time=time(12, 0))
        service = ServiceModel(headline='Haircut', name='Basic Haircut', description='A simple cut', image='img.jpg', duration_min=30, duration_max=60, price=25.0, descriptionII='Extra detail')
        service2 = ServiceModel(headline='Brading', name='Quality brading', description='A quality brading to look beauty', image='Image2.png', duration_min=25, duration_max=40, price=50.0, descriptionII='Another long description')
        team_member = TeamModel(name='John Doe', role='Stylist', image='john.jpg', bio='Experienced stylist')
        team_member2 = TeamModel(name='Paul Aquero', role='Stylist', image='paul.jpg', bio='An Extraodinary stylist')

        db.session.add_all([bt, bt2, service, service2, team_member, team_member2])
        db.session.commit()

        # Seed weekdays
        days = [
            WeekdaysModel(day_num=0, name='Monday'),
            WeekdaysModel(day_num=1, name='Tuesday'),
            WeekdaysModel(day_num=2, name='Wednesday'),
            WeekdaysModel(day_num=3, name='Thursday'),
            WeekdaysModel(day_num=4, name='Friday'),
        ]
        db.session.add_all(days)
        db.session.commit()

        # Assign workdays: John works Mon-Thu, Paul works Mon-Fri
        john_days = WeekdaysModel.query.filter(WeekdaysModel.day_num.in_([0, 1, 2, 3])).all()
        paul_days = WeekdaysModel.query.filter(WeekdaysModel.day_num.in_([0, 1, 2, 3, 4])).all()
        for day in john_days:
            db.session.add(TeamWorkdaysModel(member_id=team_member.id, day_id=day.id))
        for day in paul_days:
            db.session.add(TeamWorkdaysModel(member_id=team_member2.id, day_id=day.id))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_book_page(self):
        response = self.client.get("/book")
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.status_code,404)
        self.assertIn(b"10:00 AM", response.data)
        self.assertIn(b"12:00 PM", response.data)
        self.assertIn(b"John Doe", response.data)
        self.assertIn(b"Basic Haircut", response.data)
        self.assertIn(b"$25.0", response.data)
        self.assertIn(b"50.0", response.data)
        self.assertNotIn(b"10.0", response.data)
        self.assertIn(b"stylist", response.data)
        self.assertNotIn(b"An Extraodinary stylist", response.data)
        self.assertNotIn(b"A quality brading to look beauty", response.data)
        self.assertNotIn(b"Doesn't exist", response.data)
        self.assertIn(b"Mon", response.data)
        self.assertIn(b"Thu", response.data)
        self.assertIn(b"Fri", response.data)
        self.assertNotIn(b"Tue", response.data)
        self.assertNotIn(b"Wed", response.data)
