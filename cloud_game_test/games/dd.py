# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from testbase import TestCase
from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path


class DescribeUserGameListTestCase(ClougGameTestCaseBase):
       '''DescribeUserGameListTestCase查询用户游戏列表
   '''
   owner=ppeterzhao
   timeout=5
   priority=TestCase.EnumPriority.High
   status=TestCase.EnumStatus.Ready
 
    def run_test(self):
        #开始执行用例
        self.start_step('DescribeUserGameListTestCase查询用户游戏列表')
        params ={'gameid':''}
        resp =self.api3client.call
        self.start_step('检查返回')
        self.assert_http_ok('http状态码必须为200'，resp)

     