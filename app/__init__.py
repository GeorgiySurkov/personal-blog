from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import humanize
import os

app = Flask(__name__)
app.config.from_object(os.getenv('FLASK_CONFIG_OBJECT', 'config.BaseConfig'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


def render_field_with_validation_classes(field, **kwargs):
    if field.errors:
        kwargs['class'] += " is-invalid"
    elif field.data:
        kwargs['class'] += " is-valid"
    return field(**kwargs)


def humanize_date(date):
    humanize.i18n.activate('ru_RU')
    return humanize.naturaldate(date)


app.jinja_env.globals.update(render_field_with_validation_classes=render_field_with_validation_classes)
app.jinja_env.filters['humanize_date'] = humanize_date

from . import models, routes
