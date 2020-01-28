# -*- coding: utf-8 -*-
"""
    logbook / api v1 / roles
    ~~~~~~~~~~~~~~~~

    Role related endpoints

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify, request
from logbook import auth, logger
from logbook.models.role import Role
from logbook.api.v1 import bp


@bp.route('/roles', methods=['GET'])
@auth.login_required
def get_roles():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Role.to_json_collection(Role.query, page, per_page, 'api.get_roles')

    return jsonify(data)


"""
A role cannot be created or deleted via api. 
"""


@bp.route('/roles/<int:id>', methods=['GET'])
@auth.login_required
def get_role(id):
    # Logging
    logger.add(request.authorization.username, 'Get role ({})'.format(id))

    return jsonify(Role.query.get_or_404(id).to_json())


@bp.route('/roles/<int:id>/users', methods=['GET'])
@auth.login_required
def get_role_users(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Role.to_json_collection(Role.query.get(id).users, page, per_page, 'api.get_role_users', id=id)

    # Logging
    logger.add(request.authorization.username, 'Get role users ({})'.format(id))

    return jsonify(data)
