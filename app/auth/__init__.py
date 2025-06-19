# Blueprint defines each section of an application. It is a sub app that holds all routes, forms, and logic related to one feature.

from flask import Blueprint

auth_bp = Blueprint('auth', __name__) 
from . import routes

