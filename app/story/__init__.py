from flask import Blueprint

main = Blueprint('story', __name__)

from . import story
