# -*- coding: utf-8 -*-
"""
    logbook / Internal logging system
    ~~~~~~~~~~~~~~~~

    Handler for logging user actions, changes, etc.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from datetime import datetime
from logbook import db
from logbook.models.log import Log


def add(user, info):
    """ Adds another protocol """

    log = Log()

    log.timestamp = datetime.now()
    log.user_id = user
    log.info = info

    db.session.add(log)
    db.session.commit()
