# -*- coding: utf-8 -*-
"""
    logbook / configuration file
    ~~~~~~~~~~~~~~~~

    Global configuration settings. Includes database connection, system settings and more.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""


class Config(object):

    # logbook settings

    # Temporarily disable key sorting
    JSON_SORT_KEYS = False

    # Database settings
    # MySQL-URI: mysql://username:password@host/database
    SQLALCHEMY_DATABASE_URI = 'mysql://<username>:<password>@<host>/<database>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
