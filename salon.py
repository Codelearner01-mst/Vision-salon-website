from app import create_app, db
from flask_migrate import Migrate
from app.models import service_model, book_model, team_model, gallery_model, socials_model ,user_model
from app.models import ServiceModel, SubServiceModel, ServiceIncludesModel, AppointmentsModel, BookingTimesModel, TeamModel, SpecialtiesModel, TeamSocialsModel, GalleryModel, SocialModel, UserModel,CategoryModel
app = create_app('production')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, ServiceModel=ServiceModel, SubServiceModel=SubServiceModel, ServiceIncludesModel=ServiceIncludesModel, AppointmentsModel=AppointmentsModel, TeamModel=TeamModel, SpecialtiesModel=SpecialtiesModel, TeamSocialsModel=TeamSocialsModel, GalleryModel=GalleryModel,CategoryModel = CategoryModel, SocialModel=SocialModel, TimeModel=BookingTimesModel, UserModel=UserModel)
