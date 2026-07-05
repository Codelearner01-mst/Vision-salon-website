import unittest
from app import create_app, db, service
from app.models.service_model import ServiceModel, SubServiceModel,ServiceIncludesModel

class ServiceRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        service1 = ServiceModel(
            headline="Haircut",
            name="Basic Haircut",
            description="A simple cut",
            image="img.jpg",
            duration_min=30,
            duration_max=60,
            price=25.0,
            descriptionII="Extra detail"
        )
        service2 = ServiceModel(
            headline="Coloring",
            name="Hair Coloring",
            description="Color your hair",
            image="color.jpg",
            duration_min=60,
            duration_max=120,
            price=75.0,
            descriptionII="Extra detail"
        )
        sub_service1 = SubServiceModel(name="Trim", service_id=1)
        sub_service2 = SubServiceModel(name="Style", service_id=2)
        service_include1 = ServiceIncludesModel(name="Shampoo", service_id=2)
        service_include2 = ServiceIncludesModel(name="Conditioner", service_id=1)
        db.session.add_all([service1, service2, sub_service1, sub_service2, service_include1, service_include2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_services_page(self):
        response = self.client.get("/services")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Haircut", response.data)
        self.assertIn(b"Coloring", response.data)
        self.assertIn(b"Color your hair", response.data)
        self.assertIn(b"Trim", response.data)
        self.assertIn(b"Style", response.data)

    def test_service_detail_page(self):
        service = ServiceModel.query.first()
        response = self.client.get(f"/services/{service.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Basic Haircut", response.data)
        self.assertIn(b"Haircut", response.data)
        self.assertIn(b"Coloring", response.data)
        self.assertIn(b"Color your hair", response.data)
        self.assertNotIn(b"Shampoo", response.data)
        self.assertIn(b"Conditioner", response.data)
        self.assertIn(60, response.data)  # Check for duration_min
        self.assertIn(120, response.data)  # Check for duration_max
        ## Test for a non-existent service
        response = self.client.get("/services/999")
        self.assertEqual(response.status_code, 404)