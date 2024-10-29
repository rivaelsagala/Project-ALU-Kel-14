from flask import render_template

class GameController:

    @staticmethod
    def index():
        return render_template('index.html')
