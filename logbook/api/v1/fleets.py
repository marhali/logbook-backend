# -*- coding: utf-8 -*-
"""
    logbook / api v1 / fleets
    ~~~~~~~~~~~~~~~~

    Fleet related endpoints

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify, request, url_for
from logbook import auth, errors, info, db, logger
from logbook.models.fleet import Fleet
from logbook.models.user import User
from logbook.models.car import Car
from logbook.api.v1 import bp


@bp.route('/fleets', methods=['GET'])
@auth.login_required
def get_fleets():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Fleet.to_json_collection(Fleet.query, page, per_page, 'api.get_fleets')

    # Logging
    logger.add(request.authorization.username, 'Get all fleets ({})'.format('/fleets'))

    return jsonify(data)


@bp.route('/fleets', methods=['POST'])
@auth.login_required
def create_fleet():
    data = request.get_json() or {}

    # Request verification
    if 'id' in data:
        return errors.bad_request('Your request is invalid', 'The fleet id is automatically assigned by the system')

    if 'name' not in data:
        return errors.bad_request('Your request is invalid', 'You need to specify at least the fleet name')

    if Fleet.query.filter_by(name=data['name']).first():
        return errors.bad_request('Your request is invalid', 'The given fleet name is already in use')

    # Update database
    fleet = Fleet()
    fleet.from_json(data)

    db.session.add(fleet)
    db.session.commit()

    # Build response
    response = jsonify(fleet.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_fleet', id=fleet.id)

    # Logging
    logger.add(request.authorization.username, 'Create fleet ({})'.format(fleet))

    return response


@bp.route('/fleets/<int:id>', methods=['GET'])
@auth.login_required
def get_fleet(id):
    # Logging
    logger.add(request.authorization.username, 'Get fleet ({})'.format(id))

    return jsonify(Fleet.query.get_or_404(id))


@bp.route('/fleets/<int:id>', methods=['PUT'])
@auth.login_required
def update_fleet(id):
    fleet = Fleet.query.get_or_404(id)
    data = request.get_json() or {}

    # Request verification
    if 'id' in data and data['id'] != fleet.id:
        return errors.bad_request('Your request is invalid', 'The fleet id cannot be changed')

    if 'name' in data and data['name'] != fleet.name and Fleet.query.filter_by(name=data['name']).first():
        return errors.bad_request('Your request is invalid', 'The given fleet name is already in use')

    # Update database
    fleet.from_json(data)
    db.session.commit()

    # Logging
    logger.add(request.authorization.username, 'Update fleet ({})'.format(fleet))

    return info.ok('The fleet has been updated')


@bp.route('/fleets/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_fleet(id):
    try:
        Fleet.query.get_or_404(id).delete()
        db.session.commit()

        # Logging
        logger.add(request.authorization.username, 'Delete fleet ({})'.format(id))

        return info.ok('The fleet has been deleted')

    except Exception:
        return errors.bad_request(
            'The specified fleet cannot be deleted',
            'Fleets with references to other resources like cars or users cannot be deleted')


@bp.route('/fleets/<int:id>/users', methods=['GET'])
@auth.login_required
def get_fleet_users(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_json_collection(Fleet.query.get_or_404(id).users, page, per_page, 'api.get_fleet_users')

    # Logging
    logger.add(request.authorization.username, 'Get fleet users ({})'.format(id))

    return jsonify(data)


@bp.route('/fleets/<int:id>/users', methods=['POST'])
@auth.login_required
def add_fleet_user(id):
    data = request.get_json() or {}

    # Request verification
    if not all(k in data for k in ('fleet_id', 'user_id')):
        return errors.bad_request('Your request is invalid', 'You need to specify at least fleet- and user id')

    if not Fleet.query.get(id).first():
        return errors.bad_request('Your request is invalid', 'Cannot find given fleet id')

    if not User.query.get(data['user_id']).first():
        return errors.bad_request('Your request is invalid', 'Cannot find given user id')

    if Fleet.query.get(id).first() in User.query.get(data['user_id']).first().fleets:
        return errors.bad_request('Your request is invalid', 'The given user is already in the specified fleet')

    # Update database
    user = User.query.get(data['user_id'])
    user.fleets.add(Fleet.query.get(id))

    db.session.add(user)
    db.session.commit()

    # Logging
    logger.add(request.authorization.username, 'Add user to fleet ({})'.format(user))

    return info.ok('The user has been added')


@bp.route('/fleets/<string:fleet_id>/users/<string:user_id>', methods=['DELETE'])
@auth.login_required
def remove_fleet_user(fleet_id, user_id):
    data = request.get_json() or {}

    # Request verification
    if not all(k in data for k in ('fleet_id', 'user_id')):
        return errors.bad_request('Your request is invalid', 'You need to specify at least fleet- and user id')

    if not Fleet.query.get(id).first():
        return errors.bad_request('Your request is invalid', 'Cannot find given fleet id')

    if not User.query.get(data['user_id']).first():
        return errors.bad_request('Your request is invalid', 'Cannot find given user id')

    if not Fleet.query.get(id).first() in User.query.get(data['user_id']).first().fleets:
        return errors.bad_request('Your request is invalid', 'The given user is not in the specified fleet')

    # Update database
    user = User.query.get(data['user_id'])
    user.fleets.remove(Fleet.query.get(id))

    db.session.add(user)
    db.session.commit()

    # Logging
    logger.add(request.authorization.username, 'Remove user from fleet ({})'.format(user))

    return info.ok('The user has been removed')


@bp.route('/fleets/<int:id>/cars', methods=['GET'])
@auth.login_required
def get_fleet_cars(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Car.to_json_collection(Fleet.query.get_or_404(id).cars, page, per_page, 'api.get_fleet_cars')

    # Logging
    logger.add(request.authorization.username, 'Get fleet cars ({})'.format(id))

    return jsonify(data)


@bp.route('/fleets/<int:id>/cars', methods=['POST'])
@auth.login_required
def add_fleet_car(id):
    data = request.get_json() or {}

    # Request verification
    if not all(k in data for k in ('fleet_id', 'car_id')):
        return errors.bad_request('Your request is invalid', 'You need to specify at least fleet- and car id')

    if not Fleet.query.get(id).first():
        return errors.bad_request('Your request is invalid', 'Cannot find given fleet id')

    if not Car.query.get(data['car_id']).first():
        return errors.bad_request('Your request is invalid', 'Cannot find given car id')

    if Fleet.query.get(id).first() in Car.query.get(data['car_id']).first().fleets:
        return errors.bad_request('Your request is invalid', 'The given car is already in the specified fleet')

    # Update database
    car = Car.query.get(data['car_id'])
    car.fleets.add(Fleet.query.get(id))

    db.session.add(car)
    db.session.commit()

    # Logging
    logger.add(request.authorization.username, 'Add car to fleet ({})'.format(car))

    return info.ok('The car has been added')


@bp.route('/fleets/<string:fleet_id>/cars/<string:car_id>', methods=['DELETE'])
@auth.login_required
def remove_fleet_car(fleet_id, user_id):
    data = request.get_json() or {}

    # Request verification
    if not all(k in data for k in ('fleet_id', 'car_id')):
        return errors.bad_request('Your request is invalid', 'You need to specify at least fleet- and car id')

    if not Fleet.query.get(id).first():
        return errors.bad_request('Your request is invalid', 'Cannot find given fleet id')

    if not Car.query.get(data['car_id']).first():
        return errors.bad_request('Your request is invalid', 'Cannot find given car id')

    if not Fleet.query.get(id).first() in Car.query.get(data['car_id']).first().fleets:
        return errors.bad_request('Your request is invalid', 'The given car is not in the specified fleet')

    # Update database
    car = Car.query.get(data['car_id'])
    car.fleets.remove(Fleet.query.get(id))

    db.session.add(car)
    db.session.commit()

    # Logging
    logger.add(request.authorization.username, 'Remove car from fleet ({})'.format(car))

    return info.ok('The user has been removed')
