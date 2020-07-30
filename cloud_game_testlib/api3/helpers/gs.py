# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import time

from cloud_game_testlib.utils import get_by_path

__author__ = 'bingxili'


class Api3GSHelper(object):
    def __init__(self, client):
        self.client = client

    def list_user_games(self):
        params = {
            'GameId': ''
        }
        resp = self.client.call('DescribeUserGameList', params)
        body_json = resp.json()

        return get_by_path(body_json, 'Response.GameList', [])

    def get_user_game_by_game_id(self, game_id):
        params = {
            'GameId': game_id
        }
        resp = self.client.call('DescribeUserGameList', params)
        body_json = resp.json()
        return get_by_path(body_json, 'Response.GameList.0', None)

    def create_group(self, name, description):
        params = {
            'Name': name,
            'Description': description
        }
        resp = self.client.call('CreateGroup', params)
        body_json = resp.json()
        return get_by_path(body_json, 'Response.GroupId', None)

    def get_group(self, group_id):
        params = {
            'GroupIds.0': group_id
        }
        resp = self.client.call('DescribeGroups', params)
        body_json = resp.json()
        return get_by_path(body_json, 'Response.Groups.0', None)

    def delete_group(self, group_id):
        params = {
            'GroupId': group_id
        }
        resp = self.client.call('DeleteGroup', params)
        return resp.status_code == 200

    def list_instances(self):
        resp = self.client.call('DescribeInstances')
        body_json = resp.json()

        return get_by_path(body_json, 'Response.Instances', [])

    def pick_instance(self, names=None, regions=None, limit=1):
        params = {
            'Limit': limit
        }

        filters = []

        d = {
            'Name': names,
            'Region': regions
        }

        for filter_name, filter_values in d.items():
            if filter_values is None:
                continue

            filter_ = {
                'Name': filter_name
            }
            filters.append(filter_)
            if not isinstance(filter_values, (list, tuple)):
                filter_values = [filter_values, ]
            for i, filter_value in enumerate(filter_values):
                filter_['Values.{}'.format(i)] = filter_value

        for i, filter_ in enumerate(filters):
            for k, v in filter_.items():
                params['Filters.{}.{}'.format(i, k)] = v

        resp = self.client.call('DescribeInstances', params)
        body_json = resp.json()

        return get_by_path(body_json, 'Response.Instances.0', None)

    def get_instance(self, instance_id):
        params = {
            'InstanceIds.0': instance_id
        }
        resp = self.client.call('DescribeInstances', params)
        body_json = resp.json()
        return get_by_path(body_json, 'Response.Instances.0', None)

    def get_instance_status(self, instance_id):
        params = {
            'InstanceIds.0': instance_id
        }
        resp = self.client.call('DescribeInstancesStatus', params)
        body_json = resp.json()
        return get_by_path(body_json, 'Response.InstanceStatuses.0', None)

    def wait_instance_status(self, instance_id, condition, interval=1, timeout=30):
        start_time = time.time()
        while True:
            instance_status = self.get_instance_status(instance_id)
            if condition(instance_status):
                return True

            end_time = time.time()
            if end_time - start_time > timeout:
                return False

            time.sleep(interval)
