# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from testbase import TestCase
from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili' 


class DescribeUserGameListTestCase(ClougGameTestCaseBase):
    '''DescribeUserGameList无参数
    '''
    owner = "libingxi"
    timeout = 5
    priority = TestCase.EnumPriority.High
    status = TestCase.EnumStatus.Ready

    def run_test(self):
        # ==========
        self.start_step('DescribeUserGameList无参数')
        # TODO 这个接口设计有些奇怪, 如果开放的话, 需要修改
        params = {
            'GameId': ''
            }
        resp = self.api3client.call('DescribeUserGameList', params)
        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        body_json = resp.json()

        games = get_by_path(body_json, 'Response.GameList', None)
        self.assert_not_none('Response.GameList不为空', games)

class DescribeUserGameListByGameIdTestCase(ClougGameTestCaseBase):
    '''DescribeUserGameList根据GameId精确查询
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
        self.start_step('DescribeUserGameList根据GameId查询, GameId={}'.format(game_id))
        params = {
            'GameId': self.game_id
        }
        resp = self.api3client.call('DescribeUserGameList', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        body_json = resp.json()

        games = get_by_path(body_json, 'Response.GameList', [])
        self.assert_equal('Response.GameList只有1个', len(games), 1)

        first_game = get_by_path(body_json, 'Response.GameList.0', None)
        if self.assert_not_none('第1个游戏不为空', first_game):
            for field_name in ('GameId', 'GameName', 'Description'):
                expect_value = get_by_path(self.game, field_name)
                self.assert_eq_by_path('{}与期望游戏一致'.format(field_name), first_game, field_name, expect_value)


if __name__ == '__main__':
    # DescribeUserGameListTestCase().debug_run()
    DescribeUserGameListByGameIdTestCase().debug_run()
