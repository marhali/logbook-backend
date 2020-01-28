# -*- coding: utf-8 -*-
"""
    logbook / database models / base
    ~~~~~~~~~~~~~~~~

    Database model basics.

    :copyright: (c) 2019 Marcel Haßlinger
    :license: MIT License
"""

from flask import url_for

class PaginatedCollection(object):
    """ Represents a database model in a collection of items """

    @staticmethod
    def to_json_collection(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)

        data = {
            'items': [item.to_json() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }

        return data
