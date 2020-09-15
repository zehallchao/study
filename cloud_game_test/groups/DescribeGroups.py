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
        resp = self.api3client.call('DescribeGroups')

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
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)


###class DescribeGroupsonegroup(ClougGameTestCaseBase):
    '''DescribeGroups根据分组ID查询
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)


###class DescribeGroupsnull(ClougGameTestCaseBase):
    '''DescribeGroups，分组id为null
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)

###class DescribeGroupsmulte(ClougGameTestCaseBase):
    '''DescribeGroups，多个分组id
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)


###class DescribeGroupsfliter.groupid(ClougGameTestCaseBase):
    '''DescribeGroups，fliter.groupid=分组ID精确查找
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)


###class DescribeGroupsfliter.name(ClougGameTestCaseBase):
    '''DescribeGroups，fliter.name=分组名称精确查找
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)


###class DescribeGroupsfliter.value(ClougGameTestCaseBase):
    '''DescribeGroups，fliter.value=字符串模糊查询
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)


###class DescribeGroupsoffset(ClougGameTestCaseBase):
    '''DescribeGroups，当offset=3；limit=0
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)


###class DescribeGroupslimit(ClougGameTestCaseBase):
    '''DescribeGroups，当offset=0；limit=3
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('创建1个期望分组')
        self.group_name = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        self.group_id = self.api3_gs_helper.create_group(self.group_name, self.group_name)

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
        resp = self.api3client.call('DescribeGroups', params)

        # ==========
        self.start_step('检查返回, 与期望分组一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

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
        self.api3_gs_helper.delete_group(group_id)



if __name__ == '__main__':
    # DescribeGroupsTestCase().debug_run()
    DescribeGroupsByNameTestCase().debug_run()
