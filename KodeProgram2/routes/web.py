from flask import Blueprint, request, redirect, url_for, jsonify, session
from controller.GameController import GameController

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return GameController.index()

@web.route('/home')
def home():
    return GameController.home()

@web.route('/upload', methods=['POST'])
def upload():
    return GameController.process_image()



@web.route('/level')
def level():
    return GameController.level()

@web.route('/level1')
def level1():
    return GameController.level1()

@web.route('/check-puzzle1', methods=['POST'])
def check_puzzle1():
    return GameController.check_puzzle_state1()

@web.route('/level1/complete')
def level1_complete():
    return GameController.level1_complete()

@web.route('/level2')
def level2():
    return GameController.level2()

@web.route('/check-puzzle2', methods=['POST'])
def check_puzzle2():
    return GameController.check_puzzle_state2()

@web.route('/level2/complete')
def level2_complete():
    return GameController.level2_complete()
