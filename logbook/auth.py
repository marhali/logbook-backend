# -*- coding: utf-8 -*-
"""
    logbook / authentication services
    ~~~~~~~~~~~~~~~~

    Authentication handler for login and role checks

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from functools import wraps
from enum import Enum
from flask import request, Response
from logbook import errors
from logbook.models.user import User

import hashlib


class Role(Enum):
    """ Represents all access levels. """
    ADMIN = 100
    STANDARD = 0


def validate_credentials(username, password):
    """ Check if the given username / password combination is valid """

    u: User = User.query.filter(User.id == username).first()

    # There is no user with that username or no password set
    if not u or not u.password:
        return False

    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Compare given password with hashed database password
    return pw_hash == u.password


def validate_role(username, role: Role):
    """ Check if the given user has a specific role assigned """

    u: User = User.query.filter(User.id == username).first()

    # Compare given role with user role
    return u.role.name.upper() == role.name


def auth_header():
    """ Build a basic authentication header. """
    return Response('{"error":"Unauthorized","message":"Authentication required. '
                    'Please login with proper credentials."}', 401,
                    {'WWW-Authenticate': 'Basic realm="Logbook-Backend"'})


def login_required(f):
    """ Custom decorator to authenticate a specific request using http basic-auth. """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return auth_header()

        if not validate_credentials(auth.username, auth.password):
            return errors.unauthorized('Authentication failed. Please check your credentials.')

        return f(*args, **kwargs)
    return decorated


def role_required(role: Role):
    """ Custom decorator to check the access level of a specific user using http basic-auth. """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            username = request.authorization.username

            if not username or not validate_role(username, role):
                return errors.forbidden('Your permission level is insufficient to access the requested resource.',
                                        'To execute this request, the ' + role.name + '-Role is required')

            return f(*args, *kwargs)
        return decorated
    return decorator
