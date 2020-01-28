# -*- coding: utf-8 -*-
"""
    logbook / database models / fleet_pool
    ~~~~~~~~~~~~~~~~

    Database fleet_pool model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from logbook4bwi import db


class Fleet_Pool(db.Model):
    """ Fleet_Pool table. References fleet, car """

    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'), primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), primary_key=True)

    def __repr__(self):
        return '<Fleet_Pool fleet_id={}, car_id={}>'.format(self.fleet_id, self.car_id)
