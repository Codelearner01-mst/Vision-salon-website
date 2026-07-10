import unittest
from app import create_app, db
from app.models import ServiceModel, TeamModel, GalleryModel, CategoryModel


class TestHome(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        category = CategoryModel(name="Haircut")
        db.session.add(category)
        db.session.commit()

        service = ServiceModel(
            headline="Haircut",
            name="Basic Haircut",
            description="A simple cut",
            image="img.jpg",
            duration_min=30,
            duration_max=60,
            price=25.0,
            descriptionII="Extra detail",
        )
        service2 = ServiceModel(
            headline="Coloring",
            name="Hair Coloring",
            description="Color your hair",
            image="color.jpg",
            duration_min=60,
            duration_max=120,
            price=75.0,
            descriptionII="Extra detail",
        )
        team_member = TeamModel(
            name="John Doe",
            role="Stylist",
            image="john.jpg",
            bio="Experienced stylist",
            stylist=True,
        )
        team_member2 = TeamModel(
            name="Paul Aquero",
            role="Stylist",
            image="paul.jpg",
            bio="An Extraodinary stylist",
            stylist=True,
        )
        gallery1 = GalleryModel(
            category_id=category.id,
            image="gallery1.jpg",
            headline="Precision Bob Cut",
            subheadline="A sleek, modern bob transformation",
        )
        gallery2 = GalleryModel(
            category_id=category.id,
            image="gallery2.jpg",
            headline="Sunset Balayage",
            subheadline="Warm, dimensional color blend",
        )
        gallery3 = GalleryModel(
            category_id=category.id,
            image="gallery3.jpg",
            headline="Layered Cut",
            subheadline="Volume and movement",
        )
        db.session.add_all(
            [
                service,
                service2,
                team_member,
                team_member2,
                gallery1,
                gallery2,
                gallery3,
            ]
        )
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        self.assertIn(b"Basic Haircut", response.data)
        self.assertIn(b"Hair Coloring", response.data)
        self.assertIn(b"John Doe", response.data)
        self.assertIn(b"Paul Aquero", response.data)
        self.assertIn(b"Precision Bob Cut", response.data)
        self.assertIn(b"Sunset Balayage", response.data)
        self.assertIn(b"Layered Cut", response.data)
        self.assertIn(b"$25.0", response.data)
        self.assertIn(b"$75.0", response.data)
        self.assertIn(b"Book Now", response.data)
        self.assertIn(b"View Full Team", response.data)
        self.assertNotIn(b"Doesn't exist", response.data)