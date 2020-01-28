# -*- coding: utf-8 -*-
"""
    logbook / database models / fleet
    ~~~~~~~~~~~~~~~~

    Database fleet model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for
from logbook import db
from logbook.models import base


class Fleet(base.PaginatedCollection, db.Model):
    """ Fleet table. References fleet_pool and fleet_user """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    cars = db.relationship('Fleet_Pool', backref='pool', lazy='dynamic')
    users = db.relationship('Fleet_User', backref='fleet', lazy='dynamic')

    def __repr__(self):
        return '<Fleet id={}, name={}>'.format(self.id, self.name)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            '_links': {
                'self': url_for('api.get_fleet', id=self.id),
                'cars': url_for('api.get_fleet_cars', id=self.id),
                'users': url_for('api.get_fleet_users', id=self.id)
            }
        }

        return data

    def from_json(self, data):
        for field in ['id', 'name']:
            if field in data:
                setattr(self, field, data[field])
