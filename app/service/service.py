from . import main
from flask import app, render_template,abort
from .service_data import services_data



@main.route('/services')
def services():
    return render_template("services.html", services=services_data.values())

@main.route('/services/<int:service_id>')
def service_detail(service_id):
    service = services_data.get(service_id)
    if not service:
        abort(404)
    # Samples: all other services
    samples = [s for s in services_data.values() if s['id'] != service_id]
    return render_template("service_detail.html", service=service, samples=samples)