# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

__author__ = 'bingxili'


class API3Method(object):
    def __init__(self, params_class):
        self._params_class = params_class

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            client = getattr(instance, 'client')
            params = self._params_class(*args, **kwargs)
            return client.request(params)

        return wrapper
