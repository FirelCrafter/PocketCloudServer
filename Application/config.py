import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'pocket_cloud'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True