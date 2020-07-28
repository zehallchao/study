# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import sys
import traceback

import six
from testbase.testresult import EnumLogLevel
from testbase.util import get_last_frame_stack, smart_text

from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class AssertionMixin(object):
    def _record_assert_exception_failed(self, message=None):
        stack = get_last_frame_stack(3)
        exc_type, exc, unused_exc_traceback = sys.exc_info()
        exception_message = str(exc)[1:-1]
        msg = ("检查点不通过\n{stack}"
               "Exception \'{exception_class}\': {exception_message}\n"
               "Message: {message}".format(stack=smart_text(stack),
                                           exception_class=exc_type.__name__, exception_message=exception_message,
                                           message=smart_text(message)))
        self._TestCase__testresult.log_record(EnumLogLevel.ASSERT, msg)

    def _record_assert_equal_failed(self, message, actual, expect):
        stack = get_last_frame_stack(3)
        msg = ("检查点不通过\n{stack}{message}\n"
               "期望值：{expect_class} {expect_value}\n"
               "实际值：{actual_class} {actual_value}"
               .format(stack=smart_text(stack), message=smart_text(message),
                       expect_class=expect.__class__, expect_value=expect,
                       actual_class=actual.__class__, actual_value=actual)
               )
        self._TestCase__testresult.log_record(EnumLogLevel.ASSERT, msg)

    def assert_true(self, msg, actual):
        if bool(actual):
            return True
        self._record_assert_equal_failed(msg, actual, True)
        return False

    def assert_false(self, msg, actual):
        if not bool(actual):
            return True
        self._record_assert_equal_failed(msg, actual, False)
        return False

    def _record_assert_none_failed(self, message, actual, expect):
        stack = get_last_frame_stack(3)
        expect_value = 'None' if expect else '不为None'
        msg = ("检查点不通过\n{stack}{message}\n"
               "期望值：{expect_value}\n"
               "实际值：{actual_class} {actual_value}"
               .format(stack=smart_text(stack), message=smart_text(message),
                       expect_value=expect_value,
                       actual_class=actual.__class__, actual_value=actual)
               )
        self._TestCase__testresult.log_record(EnumLogLevel.ASSERT, msg)

    def assert_none(self, msg, actual):
        if actual is None:
            return True
        self._record_assert_none_failed(msg, actual, True)
        return False

    def assert_not_none(self, msg, actual):
        if actual is not None:
            return True
        self._record_assert_none_failed(msg, actual, False)
        return False

    def _record_assert_compare_failed(self, message, compare, actual, expect):
        stack = get_last_frame_stack(3)

        if compare not in (-2, -1, 0, 1, 2):
            raise ValueError('invalid compare')

        if compare == 1:
            # actual 大于 expect
            expect_compare = '大于'
            actual_compare = '小于等于'
        elif compare == 2:
            # actual 大于等于 expect
            expect_compare = '大于等于'
            actual_compare = '小于'
        elif compare == -1:
            # actual 小于 expect
            expect_compare = '小于'
            actual_compare = '大于等于'
        elif compare == -2:
            # actual 小于等于 expect
            expect_compare = '小于等于'
            actual_compare = '大于'
        else:
            # actual 等于 expect
            expect_compare = '等于'
            actual_compare = '不等于'

        msg = ("检查点不通过\n{stack}{message}\n"
               "期望：{actual_class} {actual_value} {expect_compare} {expect_class} {expect_value}\n"
               "实际：{actual_class} {actual_value} {actual_compare} {expect_class} {expect_value}"
               .format(stack=smart_text(stack), message=smart_text(message),
                       expect_compare=expect_compare, actual_compare=actual_compare,
                       expect_class=expect.__class__, expect_value=expect,
                       actual_class=actual.__class__, actual_value=actual)
               )
        self._TestCase__testresult.log_record(EnumLogLevel.ASSERT, msg)

    def assert_gt(self, msg, actual, expect):
        if actual > expect:
            return True
        self._record_assert_compare_failed(msg, 1, actual, expect)
        return False

    def assert_gte(self, msg, actual, expect):
        if actual > expect:
            return True
        self._record_assert_compare_failed(msg, 2, actual, expect)
        return False

    def assert_lt(self, msg, actual, expect):
        if actual > expect:
            return True
        self._record_assert_compare_failed(msg, -1, actual, expect)
        return False

    def assert_lte(self, msg, actual, expect):
        if actual > expect:
            return True
        self._record_assert_compare_failed(msg, -2, actual, expect)
        return False

    def assert_equal_by_path(self, msg, obj, path, expect):
        if isinstance(path, six.string_types):
            path = path.split('.')
        elif not isinstance(path, (list, tuple)):
            raise ValueError('path must be a list, tuple or string')

        try:
            value = get_by_path(obj, path)
            if value == expect:
                return True
            self._record_assert_equal_failed(msg, value, expect)
            return False
        except (KeyError, IndexError, AttributeError):
            self._record_assert_exception_failed(msg)
            return False

    def assert_gt_by_path(self, msg, obj, path, expect):
        if isinstance(path, six.string_types):
            path = path.split('.')
        elif not isinstance(path, (list, tuple)):
            raise ValueError('path must be a list, tuple or string')

        try:
            value = get_by_path(obj, path)
            if value > expect:
                return True
            self._record_assert_compare_failed(msg, 1, value, expect)
            return False
        except (KeyError, IndexError, AttributeError):
            self._record_assert_exception_failed(msg)
            return False

    def assert_gte_by_path(self, msg, obj, path, expect):
        if isinstance(path, six.string_types):
            path = path.split('.')
        elif not isinstance(path, (list, tuple)):
            raise ValueError('path must be a list, tuple or string')

        try:
            value = get_by_path(obj, path)
            if value >= expect:
                return True
            self._record_assert_compare_failed(msg, 2, value, expect)
            return False
        except (KeyError, IndexError, AttributeError):
            self._record_assert_exception_failed(msg)
            return False

    def assert_lt_by_path(self, msg, obj, path, expect):
        if isinstance(path, six.string_types):
            path = path.split('.')
        elif not isinstance(path, (list, tuple)):
            raise ValueError('path must be a list, tuple or string')

        try:
            value = get_by_path(obj, path)
            if value < expect:
                return True
            self._record_assert_compare_failed(msg, -1, value, expect)
            return False
        except (KeyError, IndexError, AttributeError):
            self._record_assert_exception_failed(msg)
            return False

    def assert_lte_by_path(self, msg, obj, path, expect):
        if isinstance(path, six.string_types):
            path = path.split('.')
        elif not isinstance(path, (list, tuple)):
            raise ValueError('path must be a list, tuple or string')

        try:
            value = get_by_path(obj, path)
            if value <= expect:
                return True
            self._record_assert_compare_failed(msg, -2, value, expect)
            return False
        except (KeyError, IndexError, AttributeError):
            self._record_assert_exception_failed(msg)
            return False


class HttpAssertionMixin(AssertionMixin):
    def assert_http_status_code(self, msg, response, expect):
        status_code = response.status_code
        if response.status_code != expect:
            self._record_assert_equal_failed(msg, status_code, expect)
            return False
        return True

    def assert_http_ok(self, msg, response):
        status_code = response.status_code
        if response.status_code != 200:
            self._record_assert_equal_failed(msg, status_code, 200)
            return False
        return True
