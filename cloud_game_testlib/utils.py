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
        _list_to_params(params, obj, path=path)
    elif isinstance(obj, dict):
        _dict_to_params(params, obj, path=path)
    else:
        params[path] = obj


def _list_to_params(params, objs, path=None):
    for index, obj in enumerate(objs):
        obj_path = '{}.{}'.format(path, index) if path else str(index)
        _set_value_to_params(params, obj, obj_path)


def _dict_to_params(params, d, path):
    for key, value in d.items():
        value_path = '{}.{}'.format(path, key) if path else key
        _set_value_to_params(params, value, value_path)


def obj_to_params(obj, path=None):
    params = dict()
    if _has_to_params(obj):
        _call_to_params(obj, params, path=path)
    elif isinstance(obj, (list, tuple)):
        _list_to_params(params, obj, path=path)
    elif isinstance(obj, dict):
        _dict_to_params(params, obj, path=path)
    else:
        raise ValueError('{} can not to params'.format(
            'class {}'.format(obj.__class__.__name__) if obj else 'None'
        ))
    return params


def get_by_path(obj, attr_path, *args, **kwargs):
    if not isinstance(attr_path, (list, tuple)):
        attr_path = attr_path.split('.')

    has_default = True
    if len(args) >= 1:
        default = args[0]
    elif kwargs:
        default = kwargs.get('default', None)
    else:
        default = None
        has_default = False

    cur_obj = obj
    for index, attr_name in enumerate(attr_path):
        if isinstance(cur_obj, dict):
            has_attr = dict.__contains__
            get_value = dict.get
            key_error = KeyError
        elif isinstance(cur_obj, list):
            has_attr = lambda o, k: int(k) < len(o)
            get_value = lambda o, k: o[int(k)]
            key_error = IndexError
        else:
            has_attr = hasattr
            get_value = getattr
            key_error = AttributeError

        if not has_attr(cur_obj, attr_name):
            if has_default:
                return default

            pre_key_path = '.'.join(attr_path[:index])
            raise key_error('\'{}\' has no \'{}\''.format(pre_key_path, attr_name))

        cur_obj = get_value(cur_obj, attr_name)
    return cur_obj
