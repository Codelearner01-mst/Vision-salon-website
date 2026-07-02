from flask import Blueprint

main = Blueprint('book', __name__)

from . import book
