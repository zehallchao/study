# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class DescribeInstancesTestCase(ClougGameTestCaseBase):
    '''DescribeInstances无参数
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def run_test(self):
        # ==========
        self.start_step('DescribeInstances无参数')
        resp = self.api3client.call('DescribeInstances')

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        body_json = resp.json()

        self.assert_gte_by_path('Response.Total至少为1', body_json, 'Response.Total', 1)

        instances = get_by_path(body_json, 'Response.Instances', [])
        self.assert_gte('Response.Instances至少有1个', len(instances), 1)


class DescribeInstancesByNameTestCase(ClougGameTestCaseBase):
    '''DescribeInstances根据名称模糊查询
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('通过DescribeInstances选定一个期望实例')
        instances = self.api3_gs_helper.list_instances()
        self.instance = instances[0] if instances else None
        self.instance_id = get_by_path(self.instance, 'InstanceId', None)
        self.instance_name = get_by_path(self.instance, 'Name', None)

    def run_test(self):
        instance_id = getattr(self, 'instance_id', None)
        if not instance_id:
            self.fail('选定期望实例失败, 实例列表可能为空, 或者接口返回错误')
            return

        # ==========
        self.start_step('DescribeInstances根据单个名称查询')
        params = {
            'Filters.0.Name': 'Name',
            'Filters.0.Values.0': self.instance_name,
        }
        resp = self.api3client.call('DescribeInstances', params)

        # ==========
        self.start_step('检查返回, 与期望实例一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        body_json = resp.json()

        self.assert_eq_by_path('Response.Total为1', body_json, 'Response.Total', 1)

        instances = get_by_path(body_json, 'Response.Instances', [])
        self.assert_equal('Response.Instances只有1个', len(instances), 1)

        first_instance = get_by_path(body_json, 'Response.Instances.0', None)
        if self.assert_not_none('第1个实例不为空', first_instance):
            self.assert_eq_by_path('InstanceId与期望实例一致为{}'.format(self.instance_id),
                                   first_instance, 'InstanceId', self.instance_id)
            for field_name in ('Name', 'Description', 'PublicIp', 'Region', 'Type'):
                expect_value = get_by_path(self.instance, field_name, None)
                self.assert_eq_by_path('{}与期望实例一致'.format(field_name), first_instance, field_name, expect_value)


if __name__ == '__main__':
    # DescribeInstancesTestCase().debug_run()
    DescribeInstancesByNameTestCase().debug_run()
