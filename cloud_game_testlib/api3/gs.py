# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from cloud_game_testlib.api3.complex.gs import (
    DescribeGroupsParams, CreateGroupParams, ModifyGroupParams, DeleteGroupParams
)
from cloud_game_testlib.api3.base import API3Method

__author__ = 'bingxili'


class GSAPI3(object):
    def __init__(self, client):
        self.client = client

    # groups
    DescribeGroups = API3Method(DescribeGroupsParams)

    CreateGroup = API3Method(CreateGroupParams)

    ModifyGroup = API3Method(ModifyGroupParams)

    DeleteGroup = API3Method(DeleteGroupParams)
