# -*- coding: utf-8 -*-
"""
    logbook / database models / log
    ~~~~~~~~~~~~~~~~

    Database car model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for
from logbook import db
from logbook.models import base


class Car(base.PaginatedCollection, db.Model):
    """ Car table. References journey, fleet_pool """

    id = db.Column(db.String(10), primary_key=True)
    brand = db.Column(db.String(35))
    model = db.Column(db.String(35))
    fuel = db.Column(db.String(10))
    vin = db.Column(db.String(17))
    owner = db.Column(db.String(35))
    mot = db.Column(db.Date)
    wheel = db.Column(db.String(10))
    status = db.Column(db.Boolean)
    fleets = db.relationship('Fleet_Pool', backref='cars', lazy='dynamic')
    journeys = db.relationship('Journey', backref='car', lazy='dynamic')

    def __repr__(self):
        return '<Car id={}>'.format(self.id)

    def to_json(self):
        data = {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'fuel': self.fuel,
            'vin': self.vin,
            'owner': self.owner,
            'mot': self.mot,
            'wheel': self.wheel,
            'status': self.status,
            '_links': {
                'self': url_for('api.get_car', id=self.id),
                'fleets': url_for('api.get_car_fleets', id=self.id),
                'journeys': url_for('api.get_car_journeys', id=self.id)
            }
        }

        return data

    def from_json(self, data):
        for field in ['id', 'brand', 'model', 'fuel', 'vin', 'owner', 'mot', 'wheel', 'status']:
            if field in data:
                setattr(self, field, data[field])
