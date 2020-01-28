# -*- coding: utf-8 -*-
"""
    logbook / api v1 / cars
    ~~~~~~~~~~~~~~~~

    Car related endpoints

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify, request, url_for
from logbook import auth, errors, info, db, logger
from logbook.models.car import Car
from logbook.models.fleet import Fleet
from logbook.models.journey import Journey
from logbook.api.v1 import bp


@bp.route('/cars', methods=['POST'])
@auth.login_required
def create_car():
    data = request.get_json() or {}

    # Request verification
    if 'id' not in data:
        return errors.bad_request('Your request is invalid', 'You need to specify at least the car id')

    if Car.query.filter_by(id=data['id']).first():
        return errors.bad_request('Your request is invalid', 'The given car id is already in use')

    # Update database
    car = Car()
    car.from_json(data)

    db.session.add(car)
    db.session.commit()

    # Build response
    response = jsonify(car.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_car', id=car.id)

    # Logging
    logger.add(request.authorization.username, 'Create car ({})'.format(car))

    return response


@bp.route('/cars', methods=['GET'])
@auth.login_required
def get_cars():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Car.to_json_collection(Car.query, page, per_page, 'api.get_cars')

    # Logging
    logger.add(request.authorization.username, 'Get all cars ({})'.format('/cars'))

    return jsonify(data)


@bp.route('/cars/<string:id>', methods=['GET'])
@auth.login_required
def get_car(id):
    # Logging
    logger.add(request.authorization.username, 'Get car ({})'.format(id))

    return jsonify(Car.query.get_or_404(id).to_json())


@bp.route('/cars/<string:id>', methods=['DELETE'])
@auth.login_required
@auth.role_required(auth.Role.ADMIN)
def delete_car(id):
    try:
        Car.query.get_or_404(id).delete()
        db.session.commit()

        # Logging
        logger.add(request.authorization.username, 'Delete car ({})'.format(id))

        return info.ok('The user has been deleted')

    except Exception:
        return errors.bad_request(
            'The specified car cannot be deleted',
            'Cars with references to other resources like journeys or pools cannot be deleted')


@bp.route('/cars/<string:id>', methods=['PUT'])
@auth.login_required
@auth.role_required(auth.Role.ADMIN)
def update_car(id):
    car = Car.query.get_or_404(id)
    data = request.get_json() or {}

    # Request verification
    if 'id' in data and data['id'] != car.id:
        return errors.bad_request('Your request is invalid', 'The user id cannot be changed')

    # Update database
    car.from_json(data)
    db.session.commit()

    # Logging
    logger.add(request.authorization.username, 'Update car ({})'.format(car))

    return info.ok('The car has been updated')


@bp.route('/cars/<string:id>/fleets', methods=['GET'])
@auth.login_required
def get_car_fleets(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Fleet.to_json_collection(Car.query.get_or_404(id).fleets, page, per_page, 'api.get_car_fleets')

    # Logging
    logger.add(request.authorization.username, 'Get car fleets ({})'.format(id))

    return jsonify(data)


@bp.route('/cars/<string:id>/journeys', methods=['GET'])
@auth.login_required
def get_car_journeys(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Journey.to_json_collection(Car.query.get(id).journeys, page, per_page, 'api.get_car_journeys', id=id)

    # Logging
    logger.add(request.authorization.username, 'Create car journeys ({})'.format(id))

    return jsonify(data)


@bp.route('/cars/<string:car_id>/journeys/<int:journey_id>', methods=['GET'])
@auth.login_required
def get_car_journeys_journey(car_id, journey_id):
    # Logging
    logger.add(request.authorization.username, 'Get car journey ({})'.format(id))

    return jsonify(Journey.query.get(journey_id).to_json())
