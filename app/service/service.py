from . import main
from flask import app, render_template,abort,jsonify
from app import db
from app.models.service_model import ServiceModel



@main.route('/services')
def services():
    try:
        s_arr=[]
        services = ServiceModel.query.all()
        if services is not None:
           for s in services:
              service = s.json()
              sub_services = s.sub_services
              if sub_services is not None:
                for sub_s in sub_services:
                  service["sub_works"].append(sub_s.name)
              services = s_arr
              services.append(service)
           
        return render_template("services.html", services= s_arr)
       
    except:
        return jsonify({"error": "Failed to fetch services data"})

@main.route('/services/<int:service_id>')
def service_detail(service_id):
    s = ServiceModel.query.get(service_id)
    if s is not None:
      includes = s.service_includes
      service = s.json(includes)     
      # Samples: all other services
      services = ServiceModel.query.all()
      samples = []
      for s in services:
         if s.id != service_id:
            sample = {"id": s.id, "name":s.name, "image":s.image, "desc":s.description, "price":s.price}
            samples.append(sample)
      return render_template("service_detail.html", service=service, samples=samples)
    abort(404)