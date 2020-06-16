#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_jc_api_v2
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is the test module for the project's JC API V2 module.
"""
# fmt: off
import pytest

# fmt: on
from mock import MagicMock, patch, sentinel
from jccli.jc_api_v2 import JumpcloudApiV2
from tests.utils import ObjectView


class TestJcApiV2:

    def setup_method(self, test_method):
        pass


    def teardown_method(self, test_method):
        pass

    @patch.object(JumpcloudApiV2,'get_groups')
    def test_get_groups(self, mock_get_groups):
        response = [
            ObjectView({'id': '5aa80b9f232e110d4215e3b7', 'name': 'admin', 'type': 'user_group'}),
            ObjectView({'id': '5b28760145886d16cbfd736a', 'name': 'guests', 'type': 'user_group'}),
            ObjectView({'id': '5aa81659232e110d42161565', 'name': 'dev', 'type': 'system_group'}),
            ObjectView({'id': '5c5357e0232e1164e94b2a11', 'name': 'prod', 'type': 'system_group'})
        ]
        api2 = JumpcloudApiV2("1234")
        mock_get_groups.return_value = response
        group_id, group_type = api2.get_group("guests")
        assert (
             group_id == "5b28760145886d16cbfd736a" and group_type == "user_group"
        ), "Failed to get group info"

    @patch.object(JumpcloudApiV2,'get_groups')
    def test_get_groups_not_found(self, mock_get_groups):
        response = [
            ObjectView({'id': '5c5357e0232e1164e94b2a11', 'name': 'prod', 'type': 'system_group'}),
        ]
        api2 = JumpcloudApiV2("1234")
        mock_get_groups.return_value = response
        group_id, group_type = api2.get_group("foo")
        assert (
             group_id == None and group_type == None
        ), "Group info should be None"

    def test_create_group_invalid_group(self):
        api2 = JumpcloudApiV2("1234")
        with pytest.raises(ValueError):
            api2.create_group("name", "invalid")
