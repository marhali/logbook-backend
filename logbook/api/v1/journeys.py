# -*- coding: utf-8 -*-
"""
    logbook / api v1 / journeys
    ~~~~~~~~~~~~~~~~

    Journey related endpoints

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify, request, url_for
from logbook import auth, errors, db, logger
from logbook.models.journey import Journey
from logbook.models.user import User
from logbook.api.v1 import bp


@bp.route('/journeys', methods=['POST'])
@auth.login_required
def create_journey():
    data = request.get_json() or {}

    # Request verification
    # Should we do a pre-check to require all fields?

    if 'id' or 'user_id' in data:
        return errors.bad_request(
            'Your request is invalid',
            'The journey- and creator id is automatically assigned by the system')

    # Update database
    journey = Journey
    journey.from_json(data)
    journey.user_id = User.query.get(request.authorization.username).id

    db.session.add(journey)
    db.session.commit()

    # Build response
    response = jsonify(journey.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_address', id=journey.id)

    # Logging
    logger.add(request.authorization.username, 'Create journey ({})'.format(journey))

    return response


"""
Due security reasons, it is not allowed to edit or delete journeys.
"""


@bp.route('/journeys', methods=['GET'])
@auth.login_required
def get_journeys():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Journey.to_json_collection(Journey.query, page, per_page, 'api.get_journeys')

    # Logging
    logger.add(request.authorization.username, 'Get all journeys ({})'.format('/journeys'))

    return jsonify(data)


@bp.route('/journeys/<int:id>', methods=['GET'])
@auth.login_required
def get_journey(id):
    # Logging
    logger.add(request.authorization.username, 'Get journey ({})'.format(id))

    return jsonify(Journey.query.get_or_404(id).to_json())
