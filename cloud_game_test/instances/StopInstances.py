# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import uuid

from testbase import TestCase

from cloud_game_testlib.enums import InstanceStatus
from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'ppeterzhao'


class StopInstancestestcase(ClougGameTestCaseBase):
    '''StopInstances，正常场景
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('通过DescribeInstances选定一个期望实例')
        self.instance = self.api3_gs_helper.pick_instance(names=['AUTOTEST-', ], regions=['ap-shanghai'])
        self.instance_region = get_by_path(self.instance, 'Region', None)
        self.instance_id = get_by_path(self.instance, 'InstanceId', None)

    def run_test(self):
        instance_id = getattr(self, 'instance_id', None)
        instance_region = getattr(self, 'instance_region', None)
        if not instance_id or not instance_region:
            self.fail('选定期望实例失败, 实例列表可能为空, 或者接口返回错误')
            return

        # ==========
        self.start_step('StopInstances')
        params = {
            'InstanceIds.0': self.instance_id,
            'TargetRegion': instance_region,
            'ForceReboot': True,
        }
        resp = self.api3client.call('StopInstances', params)

        # ==========
        self.start_step('检查返回, 与期望实例一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('等待实例重启完毕')
        expect_status_names = tuple(
            status.name for status in InstanceStatus.service_statuses()
        )
        def _condition(instance_status):
            status = get_by_path(instance_status, 'Status', None)
            return status in expect_status_names
        ret = self.api3_gs_helper.wait_instance_status(instance_id, _condition)
        self.assert_true('实例重启成功且没超时', ret)

        # 暂时不管变成空闲要多久
        # def _condition(instance_status):
        #     status = get_by_path(instance_status, 'Status', None)
        #     return status == InstanceStatus.IDLE.name
        # ret = self.api3_gs_helper.wait_instance_status(instance_id, _condition, timeout=5 * 60)
        # self.assert_true('实例空闲没超时', ret)


class StopInstancestestcaseregion(ClougGameTestCaseBase):
    '''StopInstances，targetregion和实际不一致
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('通过DescribeInstances选定一个期望实例')
        self.instance = self.api3_gs_helper.pick_instance(names=['AUTOTEST-', ], regions=['ap-shanghai'])
        self.instance_region = get_by_path(self.instance, 'Region', None)
        self.instance_id = get_by_path(self.instance, 'InstanceId', None)

    def run_test(self):
        instance_id = getattr(self, 'instance_id', None)
        instance_region = getattr(self, 'instance_region', None)
        if not instance_id or not instance_region:
            self.fail('选定期望实例失败, 实例列表可能为空, 或者接口返回错误')
            return

        # ==========
        self.start_step('StopInstances')
        params = {
            'InstanceIds.0': self.instance_id,
            'TargetRegion': instance_region,
            'ForceReboot': True,
        }
        resp = self.api3client.call('StopInstances', params)

        # ==========
        self.start_step('检查返回, 与期望实例一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('等待实例重启完毕')
        expect_status_names = tuple(
            status.name for status in InstanceStatus.service_statuses()
        )
        def _condition(instance_status):
            status = get_by_path(instance_status, 'Status', None)
            return status in expect_status_names
        ret = self.api3_gs_helper.wait_instance_status(instance_id, _condition)
        self.assert_true('实例重启成功且没超时', ret)




class StopInstancestestcasemanytarget(ClougGameTestCaseBase):
    '''StopInstances，多目标场景
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('通过DescribeInstances选定一个期望实例')
        self.instance = self.api3_gs_helper.pick_instance(names=['AUTOTEST-', ], regions=['ap-shanghai'])
        self.instance_region = get_by_path(self.instance, 'Region', None)
        self.instance_id = get_by_path(self.instance, 'InstanceId', None)

    def run_test(self):
        instance_id = getattr(self, 'instance_id', None)
        instance_region = getattr(self, 'instance_region', None)
        if not instance_id or not instance_region:
            self.fail('选定期望实例失败, 实例列表可能为空, 或者接口返回错误')
            return

        # ==========
        self.start_step('StopInstances')
        params = {
            'InstanceIds.0': self.instance_id,
            'TargetRegion': instance_region,
            'ForceReboot': True,
        }
        resp = self.api3client.call('StopInstances', params)

        # ==========
        self.start_step('检查返回, 与期望实例一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('等待实例重启完毕')
        expect_status_names = tuple(
            status.name for status in InstanceStatus.service_statuses()
        )
        def _condition(instance_status):
            status = get_by_path(instance_status, 'Status', None)
            return status in expect_status_names
        ret = self.api3_gs_helper.wait_instance_status(instance_id, _condition)
        self.assert_true('实例重启成功且没超时', ret)


class StopInstancestestcaseforcestop(ClougGameTestCaseBase):
    '''StopInstances，forcestop=ture
    '''
    owner = "ppeterzhao"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        # ==========
        self.start_step('通过DescribeInstances选定一个期望实例')
        self.instance = self.api3_gs_helper.pick_instance(names=['AUTOTEST-', ], regions=['ap-shanghai'])
        self.instance_region = get_by_path(self.instance, 'Region', None)
        self.instance_id = get_by_path(self.instance, 'InstanceId', None)

    def run_test(self):
        instance_id = getattr(self, 'instance_id', None)
        instance_region = getattr(self, 'instance_region', None)
        if not instance_id or not instance_region:
            self.fail('选定期望实例失败, 实例列表可能为空, 或者接口返回错误')
            return

        # ==========
        self.start_step('StopInstances')
        params = {
            'InstanceIds.0': self.instance_id,
            'TargetRegion': instance_region,
            'ForceReboot': True,
        }
        resp = self.api3client.call('StopInstances', params)

        # ==========
        self.start_step('检查返回, 与期望实例一致')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('等待实例重启完毕')
        expect_status_names = tuple(
            status.name for status in InstanceStatus.service_statuses()
        )
        def _condition(instance_status):
            status = get_by_path(instance_status, 'Status', None)
            return status in expect_status_names
        ret = self.api3_gs_helper.wait_instance_status(instance_id, _condition)
        self.assert_true('实例重启成功且没超时', ret)

if __name__ == '__main__':
    StopInstances().debug_run()