# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os
import sys


__author__ = 'bingxili'


PROJECT_NAME = "cloug_game_test"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_MODE = "standard"
INSTALLED_APPS = []
QT4S_NETWORK_RULES = ''
QT4S_NETWORK_PLUGINS = ["qt4s_ext_tencent"]
QT4S_CURRENT_AREA_DETECTORS = ["qt4s_ext_tencent.detectors.TencentCurrentAreaDetector"]


# 决定使用哪套环境的settings, 顺序为:
# 1. 环境变量QC_ENV
# 2. QTA配置drun_settings的QC_ENV
# 3. 本文件定义全局变量的QC_ENV
# 4. 默认值test
QC_ENV = 'test'


def __get_qc_env_from_drun_settings():
    try:
        import drun_settings
        return getattr(drun_settings, 'QC_ENV', None)
    except ImportError:
        return None


def __import_env_settings():
    qc_env = os.environ.get('QC_ENV', None)
    if not qc_env:
        qc_env = __get_qc_env_from_drun_settings()
    if not qc_env:
        qc_env = globals().get('QC_ENV', None)
    if not qc_env:
        qc_env = 'test'

    settings_module_name = 'settings.{}'.format(qc_env)

    __import__(settings_module_name)
    module = sys.modules[settings_module_name]
    for name in dir(module):
        if not name.startswith('__'):
            globals()[name] = getattr(module, name)


__import_env_settings()


# 请勿动, 留在最后
try:
    from drun_settings import *
except ImportError:
    pass
