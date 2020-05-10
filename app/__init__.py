from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(os.getenv('FLASK_CONFIG_OBJECT', 'config.DebugConfig'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from . import models, routes
