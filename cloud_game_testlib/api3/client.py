# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import binascii
import hashlib
import hmac
import json
import random
import time
import types

import six
from qt4s.channel.http import HttpChannel
from six.moves.urllib.parse import urlencode

from cloud_game_testlib.logging import logger as default_logger
from cloud_game_testlib.logging.adapters import BraceMessageAdapter

__author__ = 'bingxili'


def get_json_from_response(resp):
    return json.loads(resp.body.dumps())


class API3Address(object):
    def __init__(self, host, ip=None, port=80, net_area=None):
        self.host = host
        self.ip = ip
        self.port = port
        self.net_area = net_area

    def clone(self):
        return self.__class__(self.host, ip=self.ip, port=self.port, net_area=self.net_area)


class API3Signer(object):
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key

    @classmethod
    def make_message(cls, method, host, path, params):
        str_params = '&'.join(k + '=' + str(params[k]) for k in sorted(params.keys()))
        return '%s%s%s?%s' % (method.upper(), host, path, str_params)

    def sign(self, method, host, path, params):
        msg = self.make_message(method, host, path, params)
        secret_key_bytes = self.secret_key.encode('utf-8')
        msg_bytes = msg.encode('utf-8')
        hashed = hmac.new(secret_key_bytes, msg_bytes, hashlib.sha1)
        sign_bytes = binascii.b2a_base64(hashed.digest())[:-1]
        return sign_bytes.decode('utf-8')


def _ensure_signer(sign):
    if isinstance(sign, (list, tuple)):
        signer = API3Signer(*sign)
    elif isinstance(sign, (dict, )):
        signer = API3Signer(**sign)
    elif isinstance(sign, API3Signer):
        signer = sign
    else:
        raise ValueError('sign must be a list, tuple, dict or API3Signer')
    return signer


class API3Client(object):
    def __init__(self, address, version, path=None, sign=None,
                 logger=None):
        if isinstance(address, (list, tuple)):
            address = API3Address(*address)
        elif isinstance(address, (dict, )):
            address = API3Address(**address)
        elif isinstance(address, six.string_types):
            address = API3Address(address)
        elif isinstance(sign, API3Address):
            address = address
        else:
            raise ValueError('sign must be a list, tuple, dict, string or API3Address')
        self.address = address

        host = self.address.host
        ip = self.address.ip or host
        port = self.address.port or 80
        self.channel = HttpChannel((ip, port, self.address.net_area))

        self.version = version
        self.path = path or '/'

        self.signer = _ensure_signer(sign) if sign else None

        self.logger = BraceMessageAdapter(logger or default_logger)

    def inject_params(self, params, sign=None):
        signer = self.signer or _ensure_signer(sign)

        injected_params = {}
        if params:
            injected_params.update(params)
        # 这样写, 是为了不让params覆盖了injected_params
        injected_params.update({
            'Timestamp': int(time.time()) - 100,
            'SecretId': signer.secret_id,
            'Version': self.version,
            'Nonce': random.randint(0, 1000000)
        })
        return injected_params

    def sign_params(self, params, method='POST', sign=None):
        signer = self.signer or _ensure_signer(sign)

        host = self.address.host
        path = '/'

        signed_params = {}
        if params:
            signed_params.update(params)
        signed_params['Signature'] = signer.sign(method, host, path, params)
        return signed_params

    def request(self, params, sign=None):
        params = params if params is not None else {}

        signer = self.signer or _ensure_signer(sign)

        injected_params = self.inject_params(params, sign=signer)
        signed_params = self.sign_params(injected_params, sign=signer)

        host = self.address.host
        ip = self.address.ip or host
        headers = {
            'Host': host
        }
        body = urlencode(signed_params)

        self.logger.info('[request] host={host} url=http://{ip}{path}?{body}', host=host, ip=ip, path=self.path,
                         body=body)
        resp = self.channel.post(self.path, body=body, headers=headers)
        self.logger.info('[response] status_code={status_code} body={body}', status_code=resp.status_code,
                         body=resp.body)

        # bound json method to response
        if not hasattr(resp, 'json'):
            setattr(resp, 'json', types.MethodType(get_json_from_response, self))

        return resp

    def call(self, action, params=None, sign=None):
        params = params if params is not None else {}

        params_with_action = {
            'Action': action
        }
        params_with_action.update(params)

        return self.request(params_with_action, sign=sign)
