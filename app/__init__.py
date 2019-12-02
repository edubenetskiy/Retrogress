import sqlite3

from flask import Flask, g, app

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_connection(sender, **extra):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


app.appcontext_tearing_down.connect(close_connection)

from . import models
from .views.library import library
from .views.home import home
from .views.channel import blueprint

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(home)
app.register_blueprint(library, url_prefix='/library')
app.register_blueprint(blueprint, url_prefix='/channel')
