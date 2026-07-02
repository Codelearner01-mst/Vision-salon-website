from flask import Blueprint

main = Blueprint('service', __name__)

from . import service