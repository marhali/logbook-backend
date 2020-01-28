# -*- coding: utf-8 -*-
"""
    logbook / database models / log
    ~~~~~~~~~~~~~~~~

    Database address model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for
from logbook import db
from logbook.models import base


class Address(base.PaginatedCollection, db.Model):
    """ Address table. References user """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    group = db.Column(db.String(10))
    street = db.Column(db.String(35))
    number = db.Column(db.String(10))
    zipcode = db.Column(db.String(5))
    city = db.Column(db.String(35))
    user_id = db.Column(db.String(9), db.ForeignKey('user.id'))
    # TODO: Map all journeys which used this address

    def __repr__(self):
        return '<Address id={}>'.format(self.id)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'group': self.group,
            'street': self.street,
            'number': self.number,
            'zipcode': self.zipcode,
            'city': self.city,
            '_links': {
                'self': url_for('api.get_address', id=self.id),
                'user': url_for('api.get_user', id=self.user_id)
            }
        }

        return data

    def from_json(self, data):
        for field in ['id', 'name', 'group', 'street', 'number', 'zipcode', 'city']:
            if field in data:
                setattr(self, field, data[field])
