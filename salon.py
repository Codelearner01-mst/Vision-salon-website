from app import create_app, db
from flask_migrate import Migrate
from app.models import service_model, book_model, team_model, gallery_model, socials_model, time_model, user_model
from app.models import ServiceModel, SubServiceModel, ServiceIncludesModel, AppointmentsModel, TeamModel, SpecialtiesModel, TeamSocialsModel, GalleryModel, SocialModel, TimeModel, UserModel
app = create_app('default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, ServiceModel=ServiceModel, SubServiceModel=SubServiceModel, ServiceIncludesModel=ServiceIncludesModel, AppointmentsModel=AppointmentsModel, TeamModel=TeamModel, SpecialtiesModel=SpecialtiesModel, TeamSocialsModel=TeamSocialsModel, GalleryModel=GalleryModel, SocialModel=SocialModel, TimeModel=TimeModel, UserModel=UserModel)
