# -*- coding: utf-8 -*-
"""
    logbook / database models / log
    ~~~~~~~~~~~~~~~~

    Database journey model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for
from logbook import db
from logbook.models import base


class Journey(base.PaginatedCollection, db.Model):
    """ Journey table. References car, address, bill, user """

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.String(10), db.ForeignKey('car.id'))
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    address_id_start = db.Column(db.Integer, db.ForeignKey('address.id'))
    address_id_end = db.Column(db.Integer, db.ForeignKey('address.id'))
    reason = db.Column(db.String(35))
    visited = db.Column(db.String(35))
    km_start = db.Column(db.Integer)
    km_business = db.Column(db.Integer)
    km_commute = db.Column(db.Integer)
    km_private = db.Column(db.Integer)
    km_end = db.Column(db.Integer)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'))
    bill = db.relationship('Bill', back_populates='journey')
    user_id = db.Column(db.String(9), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Journey id={}, car_id={}, user_id={}>'.format(self.id, self.car_id, self.user_id)

    def to_json(self):
        data = {
            'id': self.id,
            'car_id': self.car_id,
            'time_start': self.time_start,
            'time_end': self.time_end,
            'address_id_start': self.address_id_start,
            'address_id_end': self.address_id_end,
            'reason': self.reason,
            'visited': self.visited,
            'km_start': self.km_start,
            'km_business': self.km_business,
            'km_commute': self.km_commute,
            'km_private': self.km_private,
            'km_end': self.km_end,
            'bill_id': self.bill_id,
            'user_id': self.user_id,
            '_links': {
                'self': url_for('api.get_journey', id=self.id),
                'car': url_for('api.get_car', id=self.car_id),
                'address_start': url_for('api.get_address', id=self.address_id_start),
                'address_end': url_for('api.get_address', id=self.address_id_end),
                'bill': url_for('api.get_bill', id=self.bill_id),
                'user': url_for('api.get_user', id=self.user_id)
            }
        }

        return data

    def from_json(self, data):
        array = {
            'id', 'car_id', 'time_start', 'time_end', 'address_id_start', 'address_id_end',
            'reason', 'visited', 'km_start', 'km_business', 'km_commute', 'km_private',
            'km_end', 'bill_id', 'user_id'
        }

        for field in array:
            if field in data:
                setattr(self, field, data[field])
