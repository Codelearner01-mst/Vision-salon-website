import unittest
from app import create_app, db
from app.models.gallery_model import GalleryModel, CategoryModel


class TestGallery(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        category1 = CategoryModel(name="Haircut")
        category2 = CategoryModel(name="Coloring")
        db.session.add_all([category1, category2])
        db.session.commit()

        gallery1 = GalleryModel(
            category_id=category1.id,
            image="gallery1.jpg",
            headline="Precision Bob Cut",
            subheadline="A sleek, modern bob transformation",
        )
        gallery2 = GalleryModel(
            category_id=category2.id,
            image="gallery2.jpg",
            headline="Sunset Balayage",
            subheadline="Warm, dimensional color blend",
        )
        gallery3 = GalleryModel(
            category_id=category1.id,
            image="gallery3.jpg",
            headline="Layered Cut",
            subheadline="Volume and movement",
        )
        db.session.add_all([gallery1, gallery2, gallery3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_gallery_page(self):
        response = self.client.get("/gallery")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        self.assertIn(b"Precision Bob Cut", response.data)
        self.assertIn(b"Sunset Balayage", response.data)
        self.assertIn(b"Layered Cut", response.data)
        self.assertIn(b"Haircut", response.data)
        self.assertIn(b"Coloring", response.data)
        self.assertIn(b"gallery1.jpg", response.data)
        self.assertIn(b"gallery2.jpg", response.data)
        self.assertNotIn(b"Doesn't exist", response.data)