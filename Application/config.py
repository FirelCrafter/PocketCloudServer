import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'cloud'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    PIN_CODE ='1111'
    
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True