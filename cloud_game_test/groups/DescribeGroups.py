# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import uuid

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class DescribeGroupsTestCase(ClougGameTestCaseBase):
    '''DescribeGroups无参数
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def run_test(self):
        # ==========
        self.start_step('DescribeGroups无参数')
        resp = self.api3_call('DescribeGroups')

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        body_json = resp.json()

        self.assert_gte_by_path('Response.Total至少为1', body_json, 'Response.Total', 1)

        groups = get_by_path(body_json, 'Response.Groups', [])
        self.assert_gte('Response.Groups至少有1个', len(groups), 1)

        first_group = get_by_path(body_json, 'Response.Groups.0', None)
        if self.assert_not_none('第1个分组不为空', first_group):
            self.assert_eq_by_path('第1个分组IsDefault为True', first_group, 'IsDefault', True)


class DescribeGroupsByNameTestCase(ClougGameTestCaseBase):
    '''DescribeGroups根据名称模糊查询
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        params = {
            'Name': self.group_name,
            'Description': self.group_name
        }
        resp = self.api3_call('CreateGroup', params)
        body_json = resp.json()

        self.group_id = get_by_path(body_json, 'Response.GroupId', None)

    def run_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            self.fail('创建期望分组失败')
            return

        # ==========
        self.start_step('DescribeGroups根据单个名称查询')
        params = {
            'Filters.0.Name': 'Name',
            'Filters.0.Values.0': self.group_name,
        }
        resp = self.api3_call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        body_json = resp.json()

        self.assert_eq_by_path('Response.Total为1', body_json, 'Response.Total', 1)

        groups = get_by_path(body_json, 'Response.Groups', [])
        self.assert_equal('Response.Groups只有1个', len(groups), 1)

        first_group = get_by_path(body_json, 'Response.Groups.0', None)
        if self.assert_not_none('第1个分组不为空', first_group):
            self.assert_eq_by_path('GroupId与期望分组一致为{}'.format(self.group_id), first_group, 'GroupId', self.group_id)
            for field_name in ('Name', 'Description'):
                self.assert_eq_by_path('{}与期望分组一致'.format(field_name), first_group, field_name, self.group_name)

    def post_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            return

        self.start_step('删除创建的分组')
        params = {
            'GroupId': group_id
        }
        resp = self.api3_call('DeleteGroup', params)


if __name__ == '__main__':
    # DescribeGroupsTestCase().debug_run()
    DescribeGroupsByNameTestCase().debug_run()
