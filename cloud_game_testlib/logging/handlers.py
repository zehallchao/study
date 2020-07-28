# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import logging

from testbase.testresult import EnumLogLevel

__author__ = 'bingxili'


class TestResultHandler(logging.Handler):
    level_mappings = {
        logging.DEBUG: EnumLogLevel.DEBUG,
        logging.INFO: EnumLogLevel.INFO,
        logging.WARNING: EnumLogLevel.WARNING,
        logging.ERROR: EnumLogLevel.ERROR,
    }

    def __init__(self, level=logging.NOTSET):
        super(TestResultHandler, self).__init__(level=level)

    def emit(self, record):
        if not record:
            return
        testresult = record.__dict__.get('testresult', None)
        if not testresult:
            return

        try:
            testresult = record.__dict__.get('testresult', None)
            testresult_level = self.level_mappings.get(record.levelno, EnumLogLevel.DEBUG)
            msg = self.format(record)
            testresult.log_record(testresult_level, msg)
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)
