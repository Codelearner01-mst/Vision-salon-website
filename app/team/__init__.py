from flask import Blueprint

main = Blueprint('team', __name__)

from . import team
