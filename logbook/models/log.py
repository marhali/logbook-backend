# -*- coding: utf-8 -*-
"""
    logbook / database models / log
    ~~~~~~~~~~~~~~~~

    Database log model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for
from logbook import db
from logbook.models import base


class Log(base.PaginatedCollection, db.Model):
    """ Log table. References user """

    timestamp = db.Column(db.DateTime, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    info = db.Column(db.String(255))

    def __repr__(self):
        return '<Log timestamp={}, user_id={}, info={}>'.format(self.timestamp, self.user_id, self.info)

    def to_json(self):
        data = {
            'timestamp': self.timestamp,
            'user_id': self.issuer.id,
            'info': self.info
        }

        return data

    def from_json(self, data):
        for field in ['timestamp', 'user_id', 'info']:
            if field in data:
                setattr(self, field, data[field])
