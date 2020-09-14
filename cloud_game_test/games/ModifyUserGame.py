# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import uuid

from testbase import TestCase
from cloud_game_testlib.testcase import ClougGameTestCaseBase
from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'
         
class ModifyUserGameTestCase(ClougGameTestCaseBase):
    '''ModifyUserGame
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
        self.start_step('ModifyUserGame, GameId={}'.format(game_id))
        self.game['Description'] = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        params = {
            'GameId': game_id,
            'Description': 
            self.game['Description']
        }
        resp = self.api3client.call('ModifyUserGame', params)

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('通过DescribeUserGameList获取信息, 与期望信息一致')
        game = self.api3_gs_helper.get_user_game_by_game_id(game_id)

        if self.assert_not_none('查询游戏不为空', game):
            for field_name in ('GameId', 'GameName', 'Description'):
                expect_value = get_by_path(self.game, field_name)
                self.assert_eq_by_path('{}与期望游戏一致'.format(field_name), game, field_name, expect_value)


if __name__ == '__main__':
    ModifyUserGameTestCase().debug_run()
