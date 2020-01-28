# -*- coding: utf-8 -*-
"""
    logbook / Error templates
    ~~~~~~~~~~~~~~~~

    Generic error templates formatted with JSON.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def create_response(status_code, message, details):
    header = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}

    if message:
        header['message'] = message

    if details:
        header['details'] = details

    response = jsonify(header)
    response.status_code = status_code

    return response


def bad_request(message=None, details=None):
    return create_response(400, message, details)


def unauthorized(message=None, details=None):
    return create_response(401, message, details)


def forbidden(message=None, details=None):
    return create_response(403, message, details)


def not_found(message=None, details=None):
    return create_response(404, message, details)
