from flask import Flask, render_template
from Application.views.file_view import file_blueprint
from Application.config import Config
import os

def create_app():
    template_dir = os.path.abspath('Application/templates')
    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object('Application.config.DevelopmentConfig')
    app.register_blueprint(file_blueprint)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app