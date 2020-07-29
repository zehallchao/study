# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import uuid

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase

__author__ = 'bingxili'


class ModifyGroupTestCase(ClougGameTestCaseBase):
    '''ModifyGroup, 修改分组信息
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个分组')
        group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(group_name, group_name)

    def run_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            self.fail('创建分组失败')
            return

        # ==========
        self.start_step('ModifyGroup')
        group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        params = {
            'GroupId': group_id,
            'Name': group_name,
            'Description': group_name
        }
        resp = self.api3client.call('ModifyGroup', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
    ModifyGroupTestCase().debug_run()
