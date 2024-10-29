from flask import render_template

class GameController:

    @staticmethod
    def index():
        return render_template('index.html')
    
    @staticmethod
    def home():
        return render_template('home.html')
    
    @staticmethod
    def home():
        return render_template('home.html')

