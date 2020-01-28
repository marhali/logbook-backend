# -*- coding: utf-8 -*-
"""
    logbook / api v1 / users
    ~~~~~~~~~~~~~~~~

    User related endpoints

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify, request, url_for
from logbook import auth, errors, info, db, logger
from logbook.models.user import User
from logbook.models.address import Address
from logbook.models.log import Log
from logbook.models.fleet import Fleet
from logbook.models.journey import Journey
from logbook.api.v1 import bp


@bp.route('/users', methods=['POST'])
@auth.login_required
@auth.role_required(auth.Role.ADMIN)
def create_user():
    data = request.get_json() or {}

    # Request verification
    if not all(k in data for k in ('id', 'email', 'password')):
        return errors.bad_request('Your request is invalid', 'You need to specify at least id, email and password')

    if User.query.filter_by(id=data['id']).first():
        return errors.bad_request('Your request is invalid', 'The given user id is already in use')

    if User.query.filter_by(email=data['email']).first():
        return errors.bad_request('Your request is invalid', 'The given email address is already in use')

    # Update database
    user = User()
    user.from_json(data)

    db.session.add(user)
    db.session.commit()

    # Build response
    response = jsonify(user.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)

    # Logging
    logger.add(request.authorization.username, 'Create user ({})'.format(user))

    return response


@bp.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_json_collection(User.query, page, per_page, 'api.get_users')

    # Logging
    logger.add(request.authorization.username, 'Get all users ({})'.format('/users'))

    return jsonify(data)


@bp.route('/users/<string:id>', methods=['GET'])
@auth.login_required
def get_user(id):
    # Logging
    logger.add(request.authorization.username, 'Get user ({})'.format(id))

    return jsonify(User.query.get_or_404(id).to_json())


@bp.route('/users/<string:id>', methods=['PUT'])
@auth.login_required
@auth.role_required(auth.Role.ADMIN)
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}

    # Request verification
    if 'id' in data and data['id'] != user.id:
        return errors.bad_request('Your request is invalid', 'The user id cannot be changed')

    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return errors.bad_request('Your request is invalid', 'The given email address is already in use')

    # Update database
    user.from_json(data)
    db.session.commit()

    # Logging
    logger.add(request.authorization.username, 'Update user ({})'.format(user))

    return info.ok('The user has been updated')


@bp.route('/users/<string:id>', methods=['DELETE'])
@auth.role_required(auth.Role.ADMIN)
def delete_user(id):
    try:
        User.query.get_or_404(id).delete()
        db.session.commit()

        # Logging
        logger.add(request.authorization.username, 'Delete user ({})'.format(id))

        return info.ok('The user has been deleted')

    except Exception:
        return errors.bad_request(
            'The specified user cannot be deleted',
            'Users with references to other resources like journeys or addresses cannot be deleted')


@bp.route('/users/<string:id>/fleets', methods=['GET'])
@auth.login_required
def get_user_fleets(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Fleet.to_json_collection(User.query.get_or_404(id).fleets, page, per_page, 'api.get_user_fleets')

    # Logging
    logger.add(request.authorization.username, 'Get user fleets ({})'.format(id))

    return jsonify(data)


@bp.route('/users/<string:id>/addresses', methods=['GET'])
@auth.login_required
def get_user_addresses(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Address.to_json_collection(User.query.get(id).addresses, page, per_page, 'api.get_user_addresses', id=id)

    # Logging
    logger.add(request.authorization.username, 'Get user addresses ({})'.format(id))

    return jsonify(data)


@bp.route('/users/<string:id>/logs', methods=['GET'])
@auth.login_required
def get_user_logs(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Log.to_json_collection(User.query.get(id).logs, page, per_page, 'api.get_user_logs', id=id)

    # Logging
    logger.add(request.authorization.username, 'Get user logs ({})'.format(id))

    return jsonify(data)


@bp.route('/users/<string:id>/journeys', methods=['GET'])
@auth.login_required
def get_user_journeys(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Journey.to_json_collection(User.query.get(id).journeys, page, per_page, 'api.get_user_journeys', id=id)

    # Logging
    logger.add(request.authorization.username, 'Get user journeys ({})'.format(id))

    return jsonify(data)


@bp.route('/users/<string:user_id>/journeys/<int:journey_id>', methods=['GET'])
@auth.login_required
def get_user_journeys_journey(user_id, journey_id):
    # Logging
    logger.add(request.authorization.username, 'Get user journey ({})'.format(id))

    return jsonify(Journey.query.get(journey_id).to_json())
