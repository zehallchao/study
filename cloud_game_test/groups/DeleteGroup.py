# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import uuid

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class DeleteGroupTestCase(ClougGameTestCaseBase):
    '''DeleteGroup
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个分组')
        group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        params = {
            'Name': group_name,
            'Description': group_name
        }
        resp = self.api3_call('CreateGroup', params)
        body_json = resp.json()

        self.group_id = get_by_path(body_json, 'Response.GroupId', None)

    def run_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            self.fail('创建分组失败')
            return

        # ==========
        self.start_step('DeleteGroup')
        params = {
            'GroupId': group_id
        }
        resp = self.api3_call('DeleteGroup', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('通过DescribeGroups检查已经删除')
        params = {
            'GroupIds.0': group_id
        }
        resp = self.api3_call('DescribeGroups', params)
        body_json = resp.json()

        self.assert_eq_by_path('Response.Total为0', body_json, 'Response.Total', 0)
        groups = get_by_path(body_json, 'Response.Groups', [])
        self.assert_equal('Response.Groups为空', len(groups), 0)

        self.group_id = None

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
    DeleteGroupTestCase().debug_run()
