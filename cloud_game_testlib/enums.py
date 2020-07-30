# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from enum import Enum
from types import DynamicClassAttribute

__author__ = 'bingxili'


class InstanceStatus(Enum):
    # 服务状态
    IDLE = ('IDLE', '空闲', 'SERVICE', False)
    LOCK = ('LOCK', '用户连接中', 'SERVICE', False)
    ESTABLISHED = ('ESTABLISHED', '游戏中', 'SERVICE', False)
    RECONNECT = ('RECONNECT', '重连中', 'SERVICE', False)
    CLOSED = ('CLOSED', '启动中', 'SERVICE', False)
    RESET = ('RESET', '清理恢复中', 'SERVICE', False)
    REBOOT = ('REBOOT', '清理恢复中', 'SERVICE', False)
    RECOVERY = ('RECOVERY', '清理恢复中', 'SERVICE', True)
    NOT_ALIVE = ('NOT_ALIVE', '无心跳', 'SERVICE', False)
    ERROR = ('ERROR', '错误', 'SERVICE', False)
    UNAVAILABLE = ('UNAVAILABLE', '不可用', 'SERVICE', True)

    # 机器状态
    PENDING = ('PENDING', '创建中', 'INSTANCE', False)
    LAUNCH_FAILED = ('LAUNCH_FAILED', '创建失败', 'INSTANCE', False)
    STOPPED = ('STOPPED', '关机', 'INSTANCE', False)
    STARTING = ('STARTING', '开机中', 'INSTANCE', False)
    STOPPING = ('STOPPING', '关机中', 'INSTANCE', False)
    REBOOTING = ('REBOOTING', '重启中', 'INSTANCE', False)
    SHUTDOWN = ('SHUTDOWN', '停止待销毁', 'INSTANCE', False)
    TERMINATING = ('TERMINATING', '销毁中', 'INSTANCE', False)

    def __new__(cls, value, display_name, status_type, is_transformed):
        obj = object.__new__(cls)
        setattr(obj, '_value_', value)
        setattr(obj, '_display_name_', display_name)
        setattr(obj, '_type_', status_type)
        setattr(obj, '_is_transformed_', is_transformed)
        return obj

    @DynamicClassAttribute
    def display_name(self):
        return self._display_name_

    @DynamicClassAttribute
    def is_transformed(self):
        return self._is_transformed_

    @DynamicClassAttribute
    def type(self):
        return self._type_

    @classmethod
    def service_statuses(cls):
        return [status for status in cls.__members__.values() if status.type == 'SERVICE']

    @classmethod
    def instance_statuses(cls):
        return [status for status in cls.__members__.values() if status.type == 'INSTANCE']
