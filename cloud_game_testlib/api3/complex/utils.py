# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

__author__ = 'bingxili'


def _has_to_params(obj):
    return hasattr(obj, 'to_params') and callable(getattr(obj, 'to_params'))


def _call_to_params(obj, params=None, path=None):
    to_params_method = getattr(obj, 'to_params')
    return to_params_method(params, path=path)


def _set_value_to_params(params, obj, path):
    if _has_to_params(obj):
        _call_to_params(obj, params, path=path)
    elif isinstance(obj, (list, tuple)):
        list_to_params(params, obj, path=path)
    elif isinstance(obj, dict):
        dict_to_params(params, obj, path=path)
    else:
        params[path] = obj


def obj_to_params(params, obj, path=None):
    if _has_to_params(obj):
        _call_to_params(obj, params, path=path)
    elif isinstance(obj, (list, tuple)):
        list_to_params(params, obj, path=path)
    elif isinstance(obj, dict):
        dict_to_params(params, obj, path=path)
    else:
        raise ValueError('{} can not to params'.format(
            'class {}'.format(obj.__class__.__name__) if obj else 'None'
        ))


def list_to_params(params, objs, path=None):
    for index, obj in enumerate(objs):
        obj_path = '{}.{}'.format(path, index) if path else str(index)
        _set_value_to_params(params, obj, obj_path)


def dict_to_params(params, d, path):
    for key, value in d.items():
        value_path = '{}.{}'.format(path, key) if path else key
        _set_value_to_params(params, value, value_path)