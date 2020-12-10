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
from jcapiv1 import Systemuserslist, Systemuser
from jcapiv2 import Group
import jccli.cli as cli

# fmt: on
from click.testing import CliRunner, Result
from mock import patch
from unittest.mock import patch as unittest_patch
from jccli.helpers import PAGE_LIMIT
from jccli.jc_api_v1 import JumpcloudApiV1
from jccli.jc_api_v2 import JumpcloudApiV2


MOCK_USER_GROUPS = [Group(id=str(i), name='group-%d' % (i,), type='user_group') for i in range(2*PAGE_LIMIT+2)]
MOCK_USERS_LIST = [Systemuser(username='user-%d' % (i,), email='fakeemail%d@fakesite.org' % (i,)) for i in range(1, 2 * PAGE_LIMIT + 2)]


def mock_get_users(self, content_type, accept, body, **kwargs):
    """Mock of jcapiv1.api.search_api.SearchApi.search_systemusers_post()
    """
    limit = body['limit']
    skip = body['skip']
    return Systemuserslist(results=MOCK_USERS_LIST[skip:skip+limit], total_count=len(MOCK_USERS_LIST))


def mock_groups_list(self, content_type, accept, limit, skip, filter, **kwargs):
    """Mock of groups_api.groups_list(), used for testing pagination
    """
    return MOCK_USER_GROUPS[skip:skip+limit]


class TestCli:
    def setup_method(self, test_method):
        pass

    def teardown_method(self, test_method):
        pass

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
        result: Result = runner.invoke(cli.cli, [
            "--key",
            "ASDFfakekey1234",
            "group",
            "create",
            "-n",
            "foo",
            "--user"
        ])
        assert (
            result.output.rstrip() == 'successfully created group: foo'
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
        result: Result = runner.invoke(cli.cli, [
            "--key",
            "ASDFfakekey1234",
            "group",
            "create",
            "--name",
            "foo",
            "--system"
        ])
        assert (
            result.output.rstrip() == 'successfully created group: foo'
        ), "Invalid response in output."

    @patch.object(JumpcloudApiV2,'delete_group')
    def test_delete_group(self, mock_delete_group):
        response = None
        mock_delete_group.return_value = response
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, [
            "--key",
            "ASDFfakekey1234",
            "group",
            "delete",
            "--name",
            "foo"
        ])
        assert (
            result.output.strip() == "successfully deleted group foo",
        ), "Invalid response in output."


    @patch.object(JumpcloudApiV1,'create_user')
    def test_create_user(self, mock_create_user):
        response = {
         "account_locked": "False",
         "email": "jc.tester1@sagebase.org",
         "id": "5dc0d38c1e2e5f51f2312948",
         "organization": "5a9d7329feb7f81004ecbee4",
         "username": "jctester1"}
        mock_create_user.return_value = response

        runner: CliRunner = CliRunner()
        # FIXME: This doesn't test much that is meaningful; it's going to get the same mock answer regardless of the
        #  arguments sent to the CLI invoker. I.e.: all it tests is whether the below command successfully makes a call
        #  to JumpcloudApiV1.create_user, *not* whether it is the right call or even a well-formed one.
        result: Result = runner.invoke(cli.cli,
            [
                "--key",
                "ASDFfakekey1234",
                "user",
                "create",
                "--email",
                "jc.tester1@sagebase.org",
                "--username",
                "jctester1"
            ]
        )
        assert (
            json.loads(result.output) == response
        ), "Invalid response in output."

    @patch.object(JumpcloudApiV1, 'get_user')
    def test_get_user(self, mock_get_user):
        user = {
            'firstname': 'Mary',
            'username': 'fake_user',
            'email': 'fake@fake.fake'
        }
        mock_get_user.return_value = user

        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli.cli, [
            "--key",
            "ASDFfakekey1234",
            "user",
            "get",
            "--username",
            "fake_user"
        ])
        retrieved_email = json.loads(result.output)['email']
        assert (
            retrieved_email == user['email']
        ), "Failed to retrieve correct user"

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
        result: Result = runner.invoke(
            cli.cli,
            [
                "--key",
                "ASDFfakekey1234",
                "user",
                "delete",
                "--username",
                "jctester"
            ]
        )
        assert (result.output == ''), "Invalid response in output."

    @patch.object(JumpcloudApiV1, 'set_user')
    @patch.object(JumpcloudApiV1, 'get_user_id')
    def test_set_user(self, mock_get_user_id, mock_set_user):
        mock_get_user_id.return_value = "1234"
        response = {
            "id": "1234",
            "username": "fake_user",
            "email": "fake_email@fakesite.com"
        }
        mock_set_user.return_value = response

        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(
            cli.cli,
            [
                "--key",
                "ASDFfakekey1234",
                "user",
                "set",
                "--username",
                "fake_user",
                "--email",
                "testemail@fakesite.com"
            ]
        )
        observed_response = json.loads(result.output)
        assert observed_response == response, "Failed to update user"

    @unittest_patch('jcapiv2.api.groups_api.GroupsApi.groups_list', new=mock_groups_list)
    def test_group_pagination(self):
        """Test that list-groups can handle pagination
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(
            cli.cli,
            [
                '--key',
                '1234-abcd',
                'group',
                'list',
                '--user'
            ]
        )

        observed_response = json.loads(result.output)
        assert observed_response == [group.to_dict() for group in MOCK_USER_GROUPS]

    @unittest_patch('jcapiv1.api.search_api.SearchApi.search_systemusers_post', new=mock_get_users)
    def test_user_pagination(self):
        """Test that list-users can handle pagination
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(
            cli.cli,
            [
                '--key',
                '1234-abcd',
                'user',
                'list'
            ]
        )
        observed_response = json.loads(result.output)
        assert observed_response == [user.to_dict() for user in MOCK_USERS_LIST]
