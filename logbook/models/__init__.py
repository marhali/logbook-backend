# -*- coding: utf-8 -*-
"""
    logbook / database models /
    ~~~~~~~~~~~~~~~~

    Initializer. Load all models before execution to avoid import conflicts.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

# Import all database models
from logbook.models.address import Address
from logbook.models.bill import Bill
from logbook.models.car import Car
from logbook.models.fleet import Fleet
from logbook.models.fleet_pool import Fleet_Pool
from logbook.models.fleet_user import Fleet_User
from logbook.models.journey import Journey
from logbook.models.log import Log
from logbook.models.role import Role
from logbook.models.user import User
