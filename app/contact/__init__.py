from flask import Blueprint

main = Blueprint('contact', __name__)

from . import contact
