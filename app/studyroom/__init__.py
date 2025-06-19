from flask import Blueprint
studyroom_bp = Blueprint('studyroom', __name__)
from . import routes