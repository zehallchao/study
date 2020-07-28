# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import logging

from cloud_game_testlib.logging.handlers import TestResultHandler

__author__ = 'bingxili'

__all__ = ['logger']


def __init_logger():
    logger_ = logging.getLogger('cloud_game_test.testcase')
    if not logger_.handlers:
        testresult_handler = TestResultHandler()
        logger_.addHandler(testresult_handler)
    logger_.setLevel(logging.DEBUG)
    return logger_


logger = __init_logger()
