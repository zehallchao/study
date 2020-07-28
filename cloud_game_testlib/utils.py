# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

__author__ = 'bingxili'


# def _get_by_path(obj, attr_path, attr_path_index, *args, **kwargs):
#     if isinstance(obj, dict):
#         has_attr = dict.__contains__
#         get_value = dict.get
#         key_error = KeyError
#     elif isinstance(obj, list):
#         has_attr = lambda o, k: int(k) < len(o)
#         get_value = lambda o, k: o[int(k)]
#         key_error = IndexError
#     else:
#         has_attr = hasattr
#         get_value = getattr
#         key_error = AttributeError
#
#     has_default = True
#     if len(args) > 1:
#         default = args[0]
#     elif kwargs:
#         default = kwargs.get('default', None)
#     else:
#         default = None
#         has_default = False
#
#     attr_name = attr_path[attr_path_index]
#     if not has_attr(obj, attr_name):
#         if has_default:
#             return default
#
#         pre_key_path = '.'.join(attr_path[:attr_path_index])
#         raise key_error('\'{}\' has no \'{}\''.format(pre_key_path, attr_name))
#
#     value = get_value(obj, attr_name)
#     if attr_path_index == len(attr_path) - 1:
#         return value
#     return (_get_by_path(value, attr_path, attr_path_index + 1, default)
#             if has_default else _get_by_path(value, attr_path, attr_path_index + 1))
#
#
# def get_by_path(obj, attr_path, *args, **kwargs):
#     if not isinstance(attr_path, (list, tuple)):
#         attr_path = attr_path.split('.')
#
#     return _get_by_path(obj, attr_path, 0, *args, **kwargs)


def get_by_path(obj, attr_path, *args, **kwargs):
    if not isinstance(attr_path, (list, tuple)):
        attr_path = attr_path.split('.')

    has_default = True
    if len(args) > 1:
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
