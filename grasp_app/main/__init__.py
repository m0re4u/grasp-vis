from flask import Blueprint

bp = Blueprint('main', __name__)

from grasp_app.main import routes