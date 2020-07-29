# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json
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
        resp = self.api3.DescribeUserGameList(GameId='')
        body_json = json.loads(resp.body.dumps())

        self.game = get_by_path(body_json, 'Response.GameList.0', None)
        self.game_id = get_by_path(self.game, 'GameId', None)

    def run_test(self):
        game_id = getattr(self, 'game_id', None)
        if not game_id:
            self.fail('选定期望游戏失败, 游戏列表可能为空, 或者接口返回错误')
            return

        # ==========
        self.start_step('ModifyUserGame, GameId={}'.format(game_id))
        self.game['Description'] = 'AUTOTEST-{}'.format(str(uuid.uuid4()))
        resp = self.api3.ModifyUserGame(GameId=game_id, Description=self.game['Description'])

        # ==========
        self.start_step('检查返回')
        self.assert_http_ok('HTTP状态码必须为200', resp)

        # ==========
        self.start_step('通过DescribeUserGameList获取信息, 与期望信息一致')
        resp = self.api3.DescribeUserGameList(GameId=self.game_id)
        body_json = json.loads(resp.body.dumps())

        first_game = get_by_path(body_json, 'Response.GameList.0', None)
        if self.assert_not_none('第1个游戏不为空', first_game):
            for field_name in ('GameId', 'GameName', 'Description'):
                expect_value = get_by_path(self.game, field_name)
                self.assert_eq_by_path('{}与期望游戏一致'.format(field_name), first_game, field_name, expect_value)


if __name__ == '__main__':
    ModifyUserGameTestCase().debug_run()
