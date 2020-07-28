# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import re

from testbase.conf import settings as testbase_settings

__author__ = 'bingxili'


class CloudGameSettings(object):
    def __init__(self):
        self._loaded = False

        self.api3_ip = None
        self.api3_host = None
        self.api3_version = None
        self.api3_net_area = None

        self.api3_accounts = {}

        self._ensure_loaded()

    def _ensure_loaded(self):
        if not self._loaded:
            self._load()
            self._loaded = True

    def _load(self):
        for attr_name, setting_name in (
                ('api3_ip', 'QC_API_GS_IP'),
                ('api3_host', 'QC_API_GS_HOST'),
                ('api3_version', 'QC_API_GS_VERSION'),
        ):
            value = testbase_settings.get(setting_name, None)
            setattr(self, attr_name, value)

        api3_net_area_name = testbase_settings.get('QC_API_GS_NET_AREA', None)
        if api3_net_area_name:
            from qt4s_ext_tencent import areas as net_areas
            self.api3_net_area = getattr(net_areas, api3_net_area_name, None)
            if not self.api3_net_area:
                raise ValueError('net area {} is not defined'.format(api3_net_area_name))
        else:
            self.api3_net_area = None

        for setting_name in dir(testbase_settings):
            match = re.match('QC_API_ACCOUNT_([A-Z0-9]+)_([A-Z0-9_]+)', setting_name)
            if not match:
                continue

            account_name = match.group(1)
            account_attr_name = match.group(2)

            if account_name not in self.api3_accounts:
                self.api3_accounts[account_name] = {}

            api3_account = self.api3_accounts[account_name]
            api3_account[account_attr_name] = testbase_settings.get(setting_name, None)


settings = CloudGameSettings()
