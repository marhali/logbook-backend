# -*- coding: utf-8 -*-
"""
    logbook / api v1 / bills
    ~~~~~~~~~~~~~~~~

    Bill related endpoints

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import jsonify, request, url_for
from logbook import auth, errors, db, logger
from logbook.models.bill import Bill
from logbook.api.v1 import bp


@bp.route('/bills', methods=['POST'])
@auth.login_required
def create_bill():
    data = request.get_json() or {}

    # Request verification
    if 'id' in data:
        return errors.bad_request(
            'Your request is invalid',
            'The address id is automatically assigned by the system'
        )

    # Update database
    bill = Bill()
    bill.from_json(data)

    db.session.add(bill)
    db.session.commit()

    # Build response
    response = jsonify(bill.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_bill', id=bill.id)

    # Logging
    logger.add(request.authorization.username, 'Create bill ({})'.format(bill))

    return response


"""
Due security reasons, it is not allowed to edit or delete bills.
"""


@bp.route('/bills', methods=['GET'])
@auth.login_required
def get_bills():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Bill.to_json_collection(Bill.query, page, per_page, 'api.get_bills')

    # Logging
    logger.add(request.authorization.username, 'Get all bills ({})'.format('/bills'))

    return jsonify(data)


@bp.route('/bills/<int:id>', methods=['GET'])
@auth.login_required
def get_bill(id):
    # Logging
    logger.add(request.authorization.username, 'Get bill ({})'.format(id))

    return jsonify(Bill.query.get_or_404(id).to_json())


@bp.route('/bills/<int:id>/picture', methods=['GET'])
def get_bill_picture(id):
    pic = Bill.query.get(id).picture

    # Logging
    logger.add(request.authorization.username, 'Get bill picture ({})'.format(id))

    return '<img src="' + pic.decode('utf-8') + '"/>'
