from app import db

class GalleryModel(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id") )
    image = db.Column(db.String(255), nullable=False)
    headline = db.Column(db.String(120), nullable=True)
    subheadline = db.Column(db.String(120), nullable=True)

    category = db.relationship("CategoryModel",backref = "galleries")

    def __init__(self, category_id, image, headline=None,  subheadline=None):
        self.image = image
        self.headline = headline
        self.subheadline = subheadline
        self.category_id = category_id

    def json(self):
        return {
            'id': self.id,
            'image': self.image,
            'headline': self.headline,
            'subheadline': self.subheadline,
             "category":self.category.name
        }
    
class CategoryModel(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60),nullable = True)

    def __init__(self,name):
       self.name = name