# -*- coding: utf-8 -*-
"""
    logbook / main module
    ~~~~~~~~~~~~~~~~

    Backend initializer

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

flask = Flask(__name__)
flask.config.from_object(Config)
db = SQLAlchemy(flask)

from logbook.api.v1 import bp as api_v1
flask.register_blueprint(api_v1, url_prefix='/api/v1/')

def create_app(config_class=Config):
    """ Initialize all modules and processes """

    #flask = Flask(__name__)
    #flask.config.from_object(config_class)

    #db.init_app(flask)

    # Blueprint registration
    # RESTful-API v1
    #from logbook.api.v1 import bp as api_v1
    #flask.register_blueprint(api_v1, url_prefix='/api/v1/')

    return flask

