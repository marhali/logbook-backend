# -*- coding: utf-8 -*-
"""
    logbook / database models / user model
    ~~~~~~~~~~~~~~~~

    Database role model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for
from logbook import db
from logbook.models import base


class Role(base.PaginatedCollection, db.Model):
    """ Role table. References user """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    description = db.Column(db.String(35))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role id={}>'.format(self.name)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            '_links': {
                'self': url_for('api.get_role', id=self.id),
                'users': url_for('api.get_role_users', id=self.id),
            }
        }

        return data

    def from_json(self, data):
        for field in ['id', 'name', 'description']:
            if field in data:
                setattr(self, field, data[field])
