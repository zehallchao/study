# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json

from testbase import testcase

from cloud_game_testlib.api3.client import API3Client, API3Signer
from cloud_game_testlib.asserts import HttpAssertionMixin
from cloud_game_testlib.conf import settings as cloud_game_settings
from cloud_game_testlib.logging import logger as default_logger
from cloud_game_testlib.logging.adapters import TestResultLoggerAdapter, BraceMessageAdapter

__author__ = 'bingxili'


class ClougGameTestCaseBase(HttpAssertionMixin, testcase.TestCase):
    def init_test(self, testresult):
        super(ClougGameTestCaseBase, self).init_test(testresult)

        self._parent_logger = TestResultLoggerAdapter(default_logger, testresult)
        self.logger = BraceMessageAdapter(self._parent_logger)
        self.settings = cloud_game_settings

        if 'MAIN' not in self.settings.api3_accounts:
            raise ValueError('Account \'{}\' is not set'.format('MAIN'))

        self.account = self.settings.api3_accounts['MAIN']
        self.signer = API3Signer(self.account['SECRET_ID'], self.account['SECRET_KEY'])

        self.api3client = API3Client((self.settings.api3_host, self.settings.api3_ip, None, self.settings.api3_net_area),
                                     self.settings.api3_version,
                                     sign=self.signer,
                                     logger=self._parent_logger)

    def api3_call(self, action, params=None):
        self.logger.info('调用API {action}, 参数: {params}', action=action, params=json.dumps(params))
        return self.api3client.call(action, params)
