# -*- coding: utf-8 -*-
"""
    logbook / database models / log
    ~~~~~~~~~~~~~~~~

    Database bill model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for
from logbook import db
from logbook.models import base


class Bill(base.PaginatedCollection, db.Model):
    """ Bill table. References journey """

    id = db.Column(db.Integer, primary_key=True)
    liter = db.Column(db.Numeric(10,2))
    amount = db.Column(db.Numeric(10,2))
    liter_avg = db.Column(db.Numeric(10,2))
    amount_other = db.Column(db.Numeric(10,2))
    picture = db.Column(db.Binary)
    journey = db.relationship('Journey', uselist=False, back_populates='bill')

    def __repr__(self):
        return '<Bill id={}>'.format(self.id)

    def to_json(self):
        data = {
            'id': self.id,
            'liter': self.liter,
            'amount': self.amount,
            'liter_avg': self.liter_avg,
            'amount_other': self.amount_other,
            '_links': {
                'self': url_for('api.get_bill', id=self.id),
                'picture': url_for('api.get_bill_picture', id=self.id),
                'journey': url_for('api.get_journey', id=self.journey.id)
            }
        }

        return data

    def from_json(self, data):
        for field in ['id', 'liter', 'amount', 'liter_avg', 'amount_other', 'picture']:
            if field in data:
                setattr(self, field, data[field])
