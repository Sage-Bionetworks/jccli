#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_cli
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is the test module for the project's command-line interface (CLI)
module.
"""
# fmt: off
import json
import pytest
import yaml
import jccli.cli as cli

# fmt: on
from click.testing import CliRunner, Result
from mock import MagicMock, patch, sentinel
from jccli.jc_api_v1 import JumpcloudApiV1
from jccli.jc_api_v2 import JumpcloudApiV2
import jccli.helpers as jccli_helpers
import jccli.errors as jccli_errors

class TestCli:

    def setup_method(self, test_method):
        pass


    def teardown_method(self, test_method):
        pass


    def test_create_group_with_invalid_type(self):
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ["create-group", "-n", "foo", "-t", "bar"])
        assert (
            "invalid choice" in result.output.strip()
        ), "Invalid choice should be indicated in output."

    @patch.object(JumpcloudApiV2,'create_group')
    def test_create_group_type_user(self, mock_create_group):
        response = [
            {
             'id': '5dc3248445886d6c72b9614c',
             'name': 'foo',
             'type': 'user_group'
            }
        ]
        mock_create_group.return_value = response
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ["create-group", "-n", "foo", "-t", "user"])
        assert (
            yaml.safe_load(result.output) == response
        ), "Invalid response in output."

    @patch.object(JumpcloudApiV2,'create_group')
    def test_create_group_type_system(self, mock_create_group):
        response = [
            {
             'id': '5dc3248445886d6c72b9614c',
             'name': 'foo',
             'type': 'system_group'
            }
        ]
        mock_create_group.return_value = response
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ["create-group", "--name", "foo", "--type", "system"])
        assert (
            yaml.safe_load(result.output) == response
        ), "Invalid response in output."

    @patch.object(JumpcloudApiV2,'delete_group')
    def test_delete_group(self, mock_delete_group):
        response = None
        mock_delete_group.return_value = response
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ["delete-group", "--name", "foo"])
        assert (
            result.output.strip() == "Group foo deleted",
        ), "Invalid response in output."

    def test_create_user_no_arguments(self):
        runner: CliRunner = CliRunner()
        with pytest.raises(jccli_errors.MissingRequiredArgumentError):
            runner.invoke(cli.cli, ["create-user"], catch_exceptions=False)

    @patch.object(jccli_helpers,'get_user_from_term')
    @patch.object(JumpcloudApiV1,'create_user')
    def test_create_user_json(self, mock_create_user, mock_get_user_from_term):
        mock_get_user_from_term.return_value = "jctester1"
        response = {
         "account_locked": "False",
         "email": "jc.tester1@sagebase.org",
         "id": "5dc0d38c1e2e5f51f2312948",
         "organization": "5a9d7329feb7f81004ecbee4",
         "username": "jctester1"}
        mock_create_user.return_value = response

        payload = {
         "email": "jc.tester1@sagebase.org",
         "username": "jctester1"}


        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli,
                                       ["create-user",
                                        "--json",
                                        json.dumps(payload)])
        res_out = result.output.split('\n')[1].replace("\'", "\"")
        assert (
            res_out == json.dumps(response)
        ), "Invalid response in output."

    @patch.object(jccli_helpers,'get_user_from_term')
    @patch.object(JumpcloudApiV1,'create_user')
    def test_create_user_json(self, mock_create_user, mock_get_user_from_term):
        mock_get_user_from_term.return_value = "jctester1"
        response = {
         "account_locked": "False",
         "email": "jc.tester1@sagebase.org",
         "id": "5dc0d38c1e2e5f51f2312948",
         "organization": "5a9d7329feb7f81004ecbee4",
         "username": "jctester1"}
        mock_create_user.return_value = response

        payload = {
         "email": "jc.tester1@sagebase.org",
         "username": "jctester1"}


        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli,
                                       ["create-user",
                                        "--json",
                                        json.dumps(payload)])
        res_out = result.output.split('\n')[1].replace("\'", "\"")
        assert (
            res_out == json.dumps(response)
        ), "Invalid response in output."


    @patch.object(jccli_helpers,'get_user_from_file')
    @patch.object(JumpcloudApiV1,'create_user')
    def test_create_user_file(self, mock_create_user, mock_get_user_from_file):
        mock_get_user_from_file.return_value = "jctester"
        response = {
         "account_locked": "False",
         "email": "jc.tester@sagebase.org",
         "id": "5dc0d38c1e2e5f51f2312948",
         "organization": "5a9d7329feb7f81004ecbee4",
         "username": "jctester"}
        mock_create_user.return_value = response

        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli,
                                       ["create-user",
                                        "--file",
                                        "tests/jc_test_user.json"])
        res_out = result.output.split('\n')[0].replace("\'", "\"")
        assert (
            res_out == json.dumps(response)
        ), "Invalid response in output."


    @patch.object(JumpcloudApiV1,'delete_user')
    @patch.object(JumpcloudApiV1,'get_user_id')
    def test_delete_user(self, mock_get_user_id, mock_delete_user):
        mock_get_user_id.return_value = "5dcd02a82ea0d91ad09f5bb2"
        response = {
         "account_locked": "False",
         "email": "jc.tester@sagebase.org",
         "id": "5dcd02a82ea0d91ad09f5bb2",
         "organization": "5a9d7329feb7f81004ecbee4",
         "username": "jctester"}
        mock_delete_user.return_value = response

        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli,
                                       ["delete-user",
                                        "--username",
                                        "jctester"])
        res_out = result.output.split('\n')[0].replace("\'", "\"")
        assert (
            res_out == json.dumps(response)
        ), "Invalid response in output."

    @patch.object(JumpcloudApiV1,'get_user_id')
    def test_delete_user(self, mock_get_user_id):
        mock_get_user_id.return_value = None
        runner: CliRunner = CliRunner()
        with pytest.raises(jccli_errors.SystemUserNotFoundError):
            result: Result = runner.invoke(cli.cli,
                                           ["delete-user",
                                            "--username",
                                            "jctester"],
                                           catch_exceptions=False)
