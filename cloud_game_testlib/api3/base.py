# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import types

__author__ = 'bingxili'


class API3Method(object):
    # 参考https://docs.python.org/3/howto/descriptor.html#id8

    def __init__(self, params_class):
        self._params_class = params_class

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return types.MethodType(self, obj)

    def __call__(self, *args, **kwargs):
        obj = args[0]
        client = getattr(obj, 'client')
        params = self._params_class(*args[1:], **kwargs)
        return client.request(params)
