# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

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
