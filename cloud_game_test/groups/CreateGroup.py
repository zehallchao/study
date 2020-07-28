# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from testbase import TestCase

from cloud_game_testlib.api3.complex.generics import Filter
from cloud_game_testlib.api3.gs import DescribeGroupsParams, CreateGroup, ModifyGroup
from cloud_game_testlib.testcase import ClougGameTestCaseBase

__author__ = 'bingxili'


class CreateGroupTestCase(ClougGameTestCaseBase):
    '''CreateGroup
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def run_test(self):
        self.start_step('CreateGroup')

        params = CreateGroup(Name='test', Description='test')
        resp = self.api3client.request(params)

        self.assert_equal('response status code must be 200', 200, resp.status_code)


if __name__ == '__main__':
    CreateGroupTestCase().debug_run()
