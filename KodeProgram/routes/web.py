from flask import Blueprint
from controller.GameController import GameController

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return GameController.index()
