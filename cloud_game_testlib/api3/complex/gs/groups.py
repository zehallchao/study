# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from cloud_game_testlib.api3.complex.base import APIParams

__author__ = 'bingxili'


__all__ = ['DescribeGroupsParams', 'CreateGroupParams', 'ModifyGroupParams', 'DeleteGroupParams']


class DescribeGroupsParams(APIParams):
    Action = 'DescribeGroups'

    Fields = {
        'GroupIds': tuple(),
        'Filters': tuple(),
        'Offset': tuple(),
        'Limit': tuple(),
    }


class CreateGroupParams(APIParams):
    Action = 'CreateGroup'

    Fields = {
        'Name': tuple(),
        'Description': tuple(),
    }


class ModifyGroupParams(APIParams):
    Action = 'ModifyGroup'

    Fields = {
        'GroupId': tuple(),
        'Name': tuple(),
        'Description': tuple(),
    }


class DeleteGroupParams(APIParams):
    Action = 'DeleteGroup'

    Fields = {
        'GroupId': tuple(),
    }
