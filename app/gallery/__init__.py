from flask import Blueprint

main = Blueprint('gallery', __name__)

from . import gallery
