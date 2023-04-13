import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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