# -*- coding: utf-8 -*-
"""
    logbook / api v1 / addresses
    ~~~~~~~~~~~~~~~~

    Address related endpoints

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify, request, url_for
from logbook import auth, errors, info, db, logger
from logbook.models.address import Address
from logbook.models.user import User
from logbook.api.v1 import bp


@bp.route('/addresses', methods=['POST'])
def create_address():
    data = request.get_json() or {}

    # Request verification
    if 'id' in data:
        return errors.bad_request(
            'Your request is invalid',
            'The address id is automatically assigned by the system'
        )

    if 'user_id' in data:
        return errors.bad_request(
            'Your request is invalid',
            'The address creator is automatically assigned by the system')

    # Update database
    address = Address()
    address.from_json(data)
    address.user_id = User.query.get(request.authorization.username).id

    db.session.add(address)
    db.session.commit()

    # Build response
    response = jsonify(address.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_address', id=address.id)

    # Logging
    logger.add(request.authorization.username, 'Create address ({})'.format(address))

    return response


@bp.route('/addresses', methods=['GET'])
@auth.login_required
def get_addresses():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Address.to_json_collection(Address.query, page, per_page, 'api.get_addresses')

    # Logging
    logger.add(request.authorization.username, 'Request all addresses (/addresses)')

    return jsonify(data)


@bp.route('/addresses/<int:id>', methods=['GET'])
@auth.login_required
def get_address(id):
    # Logging
    logger.add(request.authorization.username, 'Request address ({})'.format(id))

    return jsonify(Address.query.get_or_404(id).to_json())


@bp.route('/addresses/<int:id>', methods=['PUT'])
@auth.login_required
def update_address(id):
    address = Address.query.get_or_404(id)
    data = request.get_json() or {}

    # Request verification
    if 'id' in data and data['id'] != address.id:
        return errors.bad_request('Your request is invalid', 'The address id cannot be changed')

    if 'user_id' in data:
        return errors.bad_request(
            'Your request is invalid',
            'The address creator is automatically assigned by the system')

    # Update database
    address.from_json(data)
    db.session.commit()

    # Logging
    logger.add(request.authorization.username, 'Update address ({})'.format(address))

    return info.ok('The address has been updated')


@bp.route('/addresses/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_address(id):
    try:
        Address.query.get_or_404(id).delete()
        db.session.commit()

        # Logging
        logger.add(request.authorization.username, 'Delete address ({})'.format(id))

        return info.ok('The address has been deleted')

    except Exception:
        return errors.bad_request(
            'The specified address cannot be deleted',
            'Addresses with references to other resources like journeys or users cannot be deleted')
