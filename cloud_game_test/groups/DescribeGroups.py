# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json
import uuid

from testbase import TestCase

from cloud_game_testlib.api3.complex.generics import Filter
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
        resp = self.api3.DescribeGroups()

        # ==========
        self.start_step('检查HTTP状态码')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('检查组数量, 至少为1')
        body_json = json.loads(resp.body.dumps())

        self.assert_gte_by_path('Response.Total至少为1', body_json, 'Response.Total', 1)

        groups = get_by_path(body_json, 'Response.Groups', [])
        self.assert_gte('Response.Groups至少有1个', len(groups), 1)

        # ==========
        self.start_step('检查第1个组为默认组')
        first_group = get_by_path(body_json, 'Response.Groups.0', None)
        if self.assert_not_none('第1个组不为空', first_group):
            self.assert_equal_by_path('第1个组IsDefault为True', first_group, 'IsDefault', True)


class DescribeGroupsByNameTestCase(ClougGameTestCaseBase):
    '''DescribeGroups根据名称模糊查询
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个组')
        resp = self.api3.DescribeGroups()
        body_json = json.loads(resp.body.dumps())
        groups = get_by_path(body_json, 'Response.Groups', [])

        if len(groups) >= 20:
            self.fail('组数量不符合条件, 期望小于20, 实际为{}'.format(len(groups)))
            return

        self.expect_group_name = str(uuid.uuid4())

        resp = self.api3.CreateGroup(Name=self.expect_group_name, Description=self.expect_group_name)
        body_json = json.loads(resp.body.dumps())

        self.expect_group_id = get_by_path(body_json, 'Response.GroupId', None)

    def run_test(self):
        expect_group_id = getattr(self, 'expect_group_id', None)
        if not expect_group_id:
            self.fail('创建组失败')
            return

        # ==========
        self.start_step('DescribeGroups根据单个名称查询')
        resp = self.api3.DescribeGroups(Filters=[
            Filter(Name='Name', Values=[self.expect_group_name, ])
        ])

        # ==========
        self.start_step('检查HTTP状态码')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('检查组数量必须为1')
        body_json = json.loads(resp.body.dumps())

        self.assert_equal_by_path('Response.Total为1', body_json, 'Response.Total', 1)

        groups = get_by_path(body_json, 'Response.Groups', [])
        self.assert_equal('Response.Groups只有1个', len(groups), 1)

        # ==========
        self.start_step('检查与期望的组信息一致')
        first_group = get_by_path(body_json, 'Response.Groups.0', None)
        if self.assert_not_none('第1个组不为空', first_group):
            self.assert_equal_by_path('GroupId必须一致', first_group, 'GroupId', self.expect_group_id)
            self.assert_equal_by_path('Name必须一致', first_group, 'Name', self.expect_group_name)

    def post_test(self):
        if not self.expect_group_id:
            return

        self.start_step('删除创建的组')
        self.api3.DeleteGroup(GroupId=self.expect_group_id)


if __name__ == '__main__':
    DescribeGroupsByNameTestCase().debug_run()
