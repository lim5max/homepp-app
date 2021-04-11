import os
import psycopg2
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://postgres:lim55555@localhost/main'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True

    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else: SECRET_KEY = 'dhjGASD123DQAAd#%136'
    DEBUG = True
    @staticmethod
    def init_app(app):
        pass

