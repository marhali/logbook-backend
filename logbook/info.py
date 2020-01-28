# -*- coding: utf-8 -*-
"""
    logbook / Information templates
    ~~~~~~~~~~~~~~~~

    Generic information templates formatted with JSON.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def create_response(status_code, message, details):
    header = {'info': HTTP_STATUS_CODES.get(status_code, 'Unknown information')}

    if message:
        header['message'] = message

    if details:
        header['details'] = details

    response = jsonify(header)
    response.status_code = status_code

    return response


def ok(message=None, details=None):
    return create_response(200, message, details)
