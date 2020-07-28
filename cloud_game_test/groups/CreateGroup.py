# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json
import uuid

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class CreateGroupTestCase(ClougGameTestCaseBase):
    '''CreateGroup
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def run_test(self):
        # ==========
        self.start_step('CreateGroup')

        group_name = str(uuid.uuid4())
        resp = self.api3.CreateGroup(Name=group_name, Description=group_name)

        # ==========
        self.start_step('检查HTTP状态码')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('检查返回GroupId')
        body_json = json.loads(resp.body.dumps())
        group_id = get_by_path(body_json, 'Response.GroupId', None)
        self.assert_not_none('GroupId不为空', group_id)

        self.group_id = group_id

    def post_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            return

        self.start_step('删除创建的组')
        self.api3.DeleteGroup(GroupId=group_id)


if __name__ == '__main__':
    CreateGroupTestCase().debug_run()
