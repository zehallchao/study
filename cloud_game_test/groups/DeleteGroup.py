# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import uuid

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase

__author__ = 'bingxili'


class DeleteGroupTestCase(ClougGameTestCaseBase):
    '''DeleteGroup, 删除分组
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
        self.start_step('DeleteGroup')
        params = {
            'GroupId': group_id
        }
        resp = self.api3client.call('DeleteGroup', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('通过DescribeGroups获取信息, 检查已经删除')
        group = self.api3_gs_helper.get_group(group_id)
        self.assert_none('查询分组为空', group)

        self.group_id = None

    def post_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            return

        self.start_step('删除创建的分组')
        self.api3_gs_helper.delete_group(group_id)


###class DeleteGroupTestCasedefgroup(ClougGameTestCaseBase):
    '''DeleteGroup, 删除分组实例是否回到默认分组
    '''
    owner = "ppeterzhao"
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
        self.start_step('DeleteGroup')
        params = {
            'GroupId': group_id
        }
        resp = self.api3client.call('DeleteGroup', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('通过DescribeGroups获取信息, 检查已经删除')
        group = self.api3_gs_helper.get_group(group_id)
        self.assert_none('查询分组为空', group)

        self.group_id = None

    def post_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            return

        self.start_step('删除创建的分组')
        self.api3_gs_helper.delete_group(group_id)


###class DeleteGroupTestCasegroupnull(ClougGameTestCaseBase):
    '''DeleteGroup, 删除分组groupid为空
    '''
    owner = "ppeterzhao"
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
        self.start_step('DeleteGroup')
        params = {
            'GroupId': group_id
        }
        resp = self.api3client.call('DeleteGroup', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('通过DescribeGroups获取信息, 检查已经删除')
        group = self.api3_gs_helper.get_group(group_id)
        self.assert_none('查询分组为空', group)

        self.group_id = None

    def post_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            return

        self.start_step('删除创建的分组')
        self.api3_gs_helper.delete_group(group_id)


###class DeleteGroupTestCasegroupnotexs(ClougGameTestCaseBase):
    '''DeleteGroup, 删除分组groupid不存在
    '''
    owner = "ppeterzhao"
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
        self.start_step('DeleteGroup')
        params = {
            'GroupId': group_id
        }
        resp = self.api3client.call('DeleteGroup', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('通过DescribeGroups获取信息, 检查已经删除')
        group = self.api3_gs_helper.get_group(group_id)
        self.assert_none('查询分组为空', group)

        self.group_id = None

    def post_test(self):
        group_id = getattr(self, 'group_id', None)
        if not group_id:
            return

        self.start_step('删除创建的分组')
        self.api3_gs_helper.delete_group(group_id)



if __name__ == '__main__':
    DeleteGroupTestCase().debug_run()
