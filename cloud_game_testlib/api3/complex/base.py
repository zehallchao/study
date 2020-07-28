# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import six

from cloud_game_testlib.api3.complex.utils import _set_value_to_params

__author__ = 'bingxili'


class ComplexObjectOptions(object):
    def __init__(self):
        self.fields = {}


class ComplexObjectBase(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        super_new = super().__new__

        # Also ensure initialization is only performed for subclasses of Complex
        # (excluding Complex class itself).
        parents = [b for b in bases if isinstance(b, ComplexObjectBase)]
        if not parents:
            return super_new(mcs, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_attrs = {'__module__': module}
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell

        fields = attrs.pop('Fields', None)

        for obj_name, obj in list(attrs.items()):
                new_attrs[obj_name] = obj

        new_class = super_new(mcs, name, bases, new_attrs, **kwargs)

        # meta
        meta = ComplexObjectOptions()
        setattr(new_class, '_meta', meta)

        # fields
        for base in new_class.mro():
            if base not in parents or not hasattr(base, '_meta'):
                continue

            parent_fields = base._meta.fields
            if parent_fields:
                meta.fields.update(parent_fields)
        if fields:
            meta.fields.update(fields)

        return new_class


@six.add_metaclass(ComplexObjectBase)
class ComplexObject(object):
    def __init__(self, *args, **kwargs):
        for field_name, unused_ignore in self._meta.fields.items():
            field_value = kwargs.get(field_name, None)
            if field_value is not None:
                setattr(self, field_name, field_value)

    def to_params(self, params=None, path=None):
        params = {} if params is None else params

        fields = self._meta.fields
        if not fields:
            return params

        for field_name, unused_ignore in fields.items():
            field_value = getattr(self, field_name, None)
            if field_value is None:
                continue

            field_path = '{}.{}'.format(path, field_name) if path else field_name
            _set_value_to_params(params, field_value, field_path)

        return params


class APIParams(ComplexObject):
    Action = None

    def to_params(self, params=None, path=None):
        params = {} if params is None else params
        params['Action'] = self.Action

        return super().to_params(params, path)