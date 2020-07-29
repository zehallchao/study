# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json
import uuid

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class ModifyGroupTestCase(ClougGameTestCaseBase):
    '''ModifyGroup
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个分组')
        group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))

        resp = self.api3.CreateGroup(Name=group_name, Description=group_name)
        body_json = json.loads(resp.body.dumps())

        self.group_id = get_by_path(body_json, 'Response.GroupId', None)

    def run_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            self.fail('创建分组失败')
            return

        # ==========
        self.start_step('ModifyGroup')
        group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        resp = self.api3.ModifyGroup(GroupId=group_id, Name=group_name, Description=group_name)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('通过DescribeGroups获取信息, 与期望信息一致')
        resp = self.api3.DescribeGroups(GroupIds=[group_id, ])
        body_json = json.loads(resp.body.dumps())

        first_group = get_by_path(body_json, 'Response.Groups.0', None)
        if self.assert_not_none('第1个分组不为空', first_group):
            for field_name in ('Name', 'Description'):
                self.assert_eq_by_path('{}与期望分组一致'.format(field_name), first_group, field_name, group_name)

    def post_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            return

        self.start_step('删除创建的分组')
        self.api3.DeleteGroup(GroupId=group_id)


if __name__ == '__main__':
    ModifyGroupTestCase().debug_run()
