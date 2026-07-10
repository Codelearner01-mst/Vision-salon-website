import unittest
from app import create_app, db
from app.models.team_model import TeamModel, SpecialtiesModel


class TestTeam(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        team_member1 = TeamModel(
            name="John Doe",
            role="Stylist",
            image="john.jpg",
            bio="Experienced stylist",
            about="More about John Doe",
            stylist=True,
        )
        team_member2 = TeamModel(
            name="Paul Aquero",
            role="Stylist",
            image="paul.jpg",
            bio="An Extraodinary stylist",
            about="More about Paul Aquero",
            stylist=True,
        )
        db.session.add_all([team_member1, team_member2])
        db.session.commit()

        specialty1 = SpecialtiesModel(name="Balayage", member_id=team_member1.id)
        specialty2 = SpecialtiesModel(name="Keratin", member_id=team_member1.id)
        specialty3 = SpecialtiesModel(name="Coloring", member_id=team_member2.id)
        db.session.add_all([specialty1, specialty2, specialty3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_team_page(self):
        response = self.client.get("/team")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        self.assertIn(b"John Doe", response.data)
        self.assertIn(b"Paul Aquero", response.data)
        self.assertIn(b"Balayage", response.data)
        self.assertIn(b"Keratin", response.data)
        self.assertIn(b"Coloring", response.data)
        self.assertIn(b"Full Profile", response.data)
        self.assertIn(b"Experienced stylist", response.data)
        self.assertIn(b"An Extraodinary stylist", response.data)
        self.assertNotIn(b"Doesn't exist", response.data)

    def test_team_detail_page(self):
        member = TeamModel.query.first()
        self.assertIsNotNone(member)
        response = self.client.get(f"/team/{member.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"John Doe", response.data)
        self.assertIn(b"More about John Doe", response.data)
        self.assertNotIn(b"More about Paul Aquero", response.data)
        self.assertNotIn(b"Paul Aquero", response.data)
        self.assertIn(b"Balayage", response.data)
        self.assertIn(b"Keratin", response.data)
        self.assertNotIn(b"Paul Aquero", response.data)
        self.assertNotIn(b"Coloring", response.data)

        # Test for a non-existent member
        response = self.client.get("/team/999")
        self.assertEqual(response.status_code, 404)