from . import main
from flask import render_template
from ..models import ServiceModel,TeamModel,GalleryModel

@main.route('/')
def index():
    service_data = ServiceModel.query.all()
    team_data = TeamModel.query.all()
    gallery_data = GalleryModel.query.all()
    try:
       services = [s.json() for s in service_data] if service_data else []
       team = [t.json() for t in team_data] if team_data else []
       gallery = [g.json() for g in gallery_data] if gallery_data else []
       return render_template("index.html", services=services, team=team, gallery=gallery)
    except Exception as e:
        print("Failed to fetch data or error occurs in jinger blocks:", e)
        return render_template("index.html", services=[], team=[], gallery=[])
    
   