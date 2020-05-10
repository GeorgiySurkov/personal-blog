from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(os.getenv('FLASK_CONFIG_OBJECT', 'config.DebugConfig'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import models, routes
