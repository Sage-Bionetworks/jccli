#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_helpers
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is the test module for the jccli helpers module.
"""
# fmt: off
import pytest

# fmt: on
import jccli.helpers as jccli_helpers

TEST_DATA_PATH = "tests/data/"

class TestHelpers:


    def setup_method(self, test_method):
        pass

    def teardown_method(self, test_method):
        pass

    def test_get_users_from_file_no_file(self):
        with pytest.raises(FileNotFoundError):
            users = jccli_helpers.get_users_from_file(TEST_DATA_PATH+"invalid.json")

    def test_get_users_from_file_users_in_data(self):
        users = jccli_helpers.get_users_from_file(TEST_DATA_PATH+"test_data.yaml")
        assert (len(users) == 2), "Invalid number of users"

    def test_get_users_from_file_no_users_in_data(self):
        users = jccli_helpers.get_users_from_file(TEST_DATA_PATH+"test_data_no_users.json")
        assert (len(users) == 0), "Invalid number of users"

    def test_get_groups_from_file_no_file(self):
        with pytest.raises(FileNotFoundError):
            users = jccli_helpers.get_groups_from_file(TEST_DATA_PATH+"invalid.json")

    def test_get_groups_from_json_file_groups_in_data(self):
        users = jccli_helpers.get_groups_from_file(TEST_DATA_PATH+"test_data.json")
        assert (len(users) == 4), "Invalid number of groups"

    def test_get_groups_from_yaml_file_groups_in_data(self):
        users = jccli_helpers.get_groups_from_file(TEST_DATA_PATH+"test_data.yaml")
        assert (len(users) == 4), "Invalid number of groups"

    def test_get_groups_from_file_no_groups_in_data(self):
        users = jccli_helpers.get_groups_from_file(TEST_DATA_PATH+"test_data_no_groups.json")
        assert (len(users) == 0), "Invalid number of groups"

    def test_get_user_from_term_valid_json(self):
        user = jccli_helpers.get_user_from_term("{\"email\": \"jc.tester1@sagebase.org\", \"username\": \"jctester1\"}")
        assert (user['email'] == "jc.tester1@sagebase.org" and
                user['username'] =="jctester1"), "Failed to get user definition"

    def test_get_user_from_file_valid_json(self):
        user = jccli_helpers.get_user_from_term("{\"email\": \"jc.tester1@sagebase.org\", \"username\": \"jctester1\"}")
        assert (user['email'] == "jc.tester1@sagebase.org" and
                user['username'] =="jctester1"), "Failed to get user definition"
