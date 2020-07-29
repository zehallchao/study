# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from testbase import TestCase

from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class DescribeGameRequirementsTestCase(ClougGameTestCaseBase):
    '''DescribeGameRequirements, 查询游戏运行要求
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def pre_test(self):
        self.start_step('通过DescribeUserGameList选定一个期望游戏')
        games = self.api3_gs_helper.list_user_games()
        self.game = games[0] if games else None
        self.game_id = get_by_path(self.game, 'GameId', None)

    def run_test(self):
        game_id = getattr(self, 'game_id', None)
        if not game_id:
            self.fail('选定期望游戏失败, 游戏列表可能为空, 或者接口返回错误')
            return

        # ==========
        self.start_step('DescribeGameRequirements, GameId={}'.format(game_id))
        params = {
            'GameId': self.game_id
        }
        resp = self.api3client.call('DescribeGameRequirements', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        body_json = resp.json()

        # 注意, 这里返回的是游戏运行要求, 跟游戏的InstanceType顺序不一定一致
        instance_candidates = get_by_path(body_json, 'Response.InstanceCandidates', None)
        self.assert_not_none('Response.InstanceCandidates不为空', instance_candidates)


if __name__ == '__main__':
    DescribeGameRequirementsTestCase().debug_run()
