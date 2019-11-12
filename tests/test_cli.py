#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_cli
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is the test module for the project's command-line interface (CLI)
module.
"""
# fmt: off

import yaml
import jccli.cli as cli
from jccli import __version__
# fmt: on
from click.testing import CliRunner, Result
from mock import MagicMock, patch, sentinel
from jccli.jc_api_v2 import JumpcloudApiV2

class TestCli:

    def setup_method(self, test_method):
        pass


    def teardown_method(self, test_method):
        pass


    def test_version_displays_library_version(self):
        """
        Arrange/Act: Run the `version` subcommand.
        Assert: The output matches the library version.
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ["version"])
        assert (
            __version__ in result.output.strip()
        ), "Version number should match library version."


    def test_verbose_output(self):
        """
        Arrange/Act: Run the `version` subcommand with the '-v' flag.
        Assert: The output indicates verbose logging is enabled.
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ["-v", "version"])
        assert (
            "Verbose" in result.output.strip()
        ), "Verbose logging should be indicated in output."


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
        result: Result = runner.invoke(cli.cli, ["create-group", "-n", "foo", "-t", "system"])
        assert (
            yaml.safe_load(result.output) == response
        ), "Invalid response in output."

    @patch.object(JumpcloudApiV2,'delete_group')
    def test_delete_group(self, mock_create_group):
        response = None
        mock_create_group.return_value = response
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, ["delete-group", "-n", "foo"])
        assert (
            result.output.strip() == "Group foo deleted",
        ), "Invalid response in output."
