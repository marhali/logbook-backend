# -*- coding: utf-8 -*-
"""
    logbook / database models / fleet_user
    ~~~~~~~~~~~~~~~~

    Database fleet_user model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from logbook4bwi import db


class Fleet_User(db.Model):
    """ Fleet_User table. References fleet, user """

    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), primary_key=True)
    user_id = db.Column(db.String(9), db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return '<Fleet_User fleet_id={}, user_id={}>'.format(self.fleet_id, self.user_id)
