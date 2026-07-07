from flask import Blueprint

main = Blueprint('main', __name__)

from . import home
from . import story
from . import contact
from . import gallery