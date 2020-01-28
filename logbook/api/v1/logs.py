# -*- coding: utf-8 -*-
"""
    logbook / api v1 / logs
    ~~~~~~~~~~~~~~~~

    Log related endpoints

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify, request
from logbook import auth, logger
from logbook.models.log import Log
from logbook.api.v1 import bp


"""
Logs can only be read by api users. The protocol is written by the backend.
"""


@bp.route('/logs', methods=['GET'])
@auth.login_required
def get_logs():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Log.to_json_collection(Log.query, page, per_page, 'api.get_users')

    # Logging
    logger.add(request.authorization.username, 'Get all logs ({})'.format('/logs'))

    return jsonify(data)
