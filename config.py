import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = 'BRUHBRUHBRUHBRUHBRUHBRUHBRUHBRUHBRUHBRUHBRUH'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

