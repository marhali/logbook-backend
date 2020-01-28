# -*- coding: utf-8 -*-
"""
    logbook / api v1
    ~~~~~~~~~~~~~~~~

    Application Programming Interface, version 1

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import Blueprint


bp = Blueprint('api', __name__)

# Import all endpoints
from logbook4bwi.api.v1 import users
from logbook4bwi.api.v1 import addresses
from logbook4bwi.api.v1 import logs
from logbook4bwi.api.v1 import journeys
from logbook4bwi.api.v1 import cars
from logbook4bwi.api.v1 import bills
from logbook4bwi.api.v1 import roles
from logbook4bwi.api.v1 import fleets
