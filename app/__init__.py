from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
import os

app = Flask(__name__)
app.config.from_object(os.getenv('FLASK_CONFIG_OBJECT', 'config.BaseConfig'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)


def render_field_with_validation_classes(field, **kwargs):
    if field.errors:
        kwargs['class'] += " is-invalid"
    elif field.data:
        kwargs['class'] += " is-valid"
    return field(**kwargs)


app.jinja_env.globals.update(render_field_with_validation_classes=render_field_with_validation_classes)

from . import models, routes
