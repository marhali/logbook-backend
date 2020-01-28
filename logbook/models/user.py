# -*- coding: utf-8 -*-
"""
    logbook / database models / user model
    ~~~~~~~~~~~~~~~~

    Database user model using SQL-Alchemy ORM.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for
from logbook import db
from logbook.models import base


class User(base.PaginatedCollection, db.Model):
    """ User table. References log, journey, address """

    id = db.Column(db.String(9), primary_key=True)
    first_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))
    email = db.Column(db.String(254))
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    status = db.Column(db.Boolean)
    logs = db.relationship('Log', backref='issuer', lazy='dynamic')
    fleets = db.relationship('Fleet_User', backref='users', lazy='dynamic')
    journeys = db.relationship('Journey', backref='driver', lazy='dynamic')
    addresses = db.relationship('Address', backref='creator', lazy='dynamic')

    def __repr__(self):
        return '<User id={}>'.format(self.id)

    def to_json(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            # Do not add hashed password to json representation
            #'password': self.password,
            'role_id': self.role_id,
            'status': self.status,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'role': url_for('api.get_role', id=self.role_id),
                'fleets': url_for('api.get_user_fleets', id=self.id),
                'journeys': url_for('api.get_user_journeys', id=self.id),
                'addresses': url_for('api.get_user_addresses', id=self.id),
                'logs': url_for('api.get_user_logs', id=self.id)
            }
        }
        return data

    def from_json(self, data):
        for field in ['id', 'first_name', 'last_name', 'email', 'password', 'role_id', 'status']:
            if field in data:
                setattr(self, field, data[field])

