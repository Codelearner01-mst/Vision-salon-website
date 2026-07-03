from app import db

class GalleryModel(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    headline = db.Column(db.String(120), nullable=True)
    subheadline = db.Column(db.String(120), nullable=True)

    def __init__(self, image, headline=None,  subheadline=None):
        self.image = image
        self.headline = headline
        self.subheadline = subheadline

    def json(self):
        return {
            'id': self.id,
            'image': self.image,
            'headline': self.headline,
            'subheadline': self.subheadline,
        }