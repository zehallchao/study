# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import logging

__author__ = 'bingxili'


class TestResultLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, testresult):
        super(TestResultLoggerAdapter, self).__init__(logger, {'testresult': testresult})


class BraceMessage:
    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)


class BraceMessageAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(BraceMessageAdapter, self).__init__(logger, extra or {})

    def log(self, level, msg, *args, exc_info=False, **kwargs):
        if self.isEnabledFor(level):
            msg_kwargs = kwargs.copy()
            msg, kwargs = self.process(msg, kwargs)
            self.logger.log(level, BraceMessage(msg, *args, **msg_kwargs), exc_info=exc_info)
