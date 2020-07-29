# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from cloud_game_testlib.api3.complex.base import APIParams

__author__ = 'bingxili'

__all__ = ['DescribeUserGameListParams', 'DescribeGameRequirementsParams', 'ModifyUserGameParams']


class DescribeUserGameListParams(APIParams):
    Action = 'DescribeUserGameList'

    Fields = {
        'GameId': tuple(),
    }


class DescribeGameRequirementsParams(APIParams):
    Action = 'DescribeGameRequirements'

    Fields = {
        'GameId': tuple(),
    }


class ModifyUserGameParams(APIParams):
    Action = 'ModifyUserGame'

    Fields = {
        'GameId': tuple(),
        'Description': tuple(),
        'State': tuple(),
        'InstanceType': tuple(),
        'CoverUrl': tuple(),
    }
