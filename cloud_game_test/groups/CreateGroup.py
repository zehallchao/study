# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import uuid

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class CreateGroupTestCase(ClougGameTestCaseBase):
    '''CreateGroup, 创建分组
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def run_test(self):
        # ==========
        self.start_step('CreateGroup')
        group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        params = {
            'Name': group_name,
            'Description': group_name
        }
        resp = self.api3client.call('CreateGroup', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        body_json = resp.json()
        group_id = get_by_path(body_json, 'Response.GroupId', None)
        self.assert_not_none('Response.GroupId不为空', group_id)

        self.group_id = group_id

        # ==========
        self.start_step('通过DescribeGroups获取信息, 与期望信息一致')
        group = self.api3_gs_helper.get_group(group_id)
        if self.assert_not_none('查询分组不为空', group):
            for field_name in ('Name', 'Description'):
                self.assert_eq_by_path('{}与期望分组一致'.format(field_name), group, field_name, group_name)

    def post_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            return

        self.start_step('删除创建的分组')
        self.api3_gs_helper.delete_group(group_id)


if __name__ == '__main__':
    CreateGroupTestCase().debug_run()
