#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_jc_api_v1
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is the test module for the project's JC API V1 module.
"""
# fmt: off
import pytest
import jcapiv1

# fmt: on
from jcapiv1 import Systemuserreturn, Systemuserslist
from mock import MagicMock, patch, sentinel
from jccli.jc_api_v1 import JumpcloudApiV1
from jccli.errors import SystemUserNotFoundError
from unit_tests.utils import ObjectView

class TestJcApiV1:

    def setup_method(self, test_method):
        pass

    def teardown_method(self, test_method):
        pass

    @patch.object(JumpcloudApiV1, 'search_users')
    def test_get_user_id(self, mock_search_users):
        mock_search_users.return_value = [
            {
                'account_locked': False,
                'activated': False,
                'addresses': [],
                'allow_public_key': True,
                'attributes': [{'name': 'nick', 'value': 'jcman'}],
                'bad_login_attempts': 0,
                'company': None,
                'cost_center': None,
                'created': '2019-11-05T01:42:36.652Z',
                'department': None,
                'description': None,
                'displayname': None,
                'email': 'jc.tester1@sagebase.org',
                'employee_identifier': None,
                'employee_type': None,
                'enable_managed_uid': False,
                'enable_user_portal_multifactor': False,
                'external_dn': None,
                'external_source_type': None,
                'externally_managed': False,
                'firstname': 'JC',
                'id': '5dc0d38c1e2e5f51f2312948',
                'job_title': None,
                'lastname': 'Tester1',
                'ldap_binding_user': False,
                'location': None,
                'mfa': {'configured': False, 'exclusion': False, 'exclusion_until': None},
                'middlename': None,
                'organization': '5a9d7329feb7f81004ecbee4',
                'password_expiration_date': None,
                'password_expired': False,
                'password_never_expires': False,
                'passwordless_sudo': False,
                'phone_numbers': [],
                'public_key': None,
                'relationships': [],
                'samba_service_user': False,
                'ssh_keys': [],
                'sudo': False,
                'tags': None,
                'totp_enabled': False,
                'unix_guid': 5109,
                'unix_uid': 5109,
                'username': 'jctester1',
            }
        ]
        api1 = JumpcloudApiV1("1234")
        user_id = api1.get_user_id("jctester1")
        assert (
             user_id == "5dc0d38c1e2e5f51f2312948"
        ), "Failed to get the user ID"

    @patch.object(JumpcloudApiV1, 'search_users')
    def test_get_user_id_not_found(self, mock_search_users):
        response = [
            {
                'email': 'jc.tester1@sagebase.org',
                'firstname': 'JC',
                'lastname': 'Tester1',
                'username': 'jctester1'
            }
        ]
        api1 = JumpcloudApiV1("1234")
        mock_search_users.return_value = response
        with pytest.raises(SystemUserNotFoundError):
            api1.get_user_id("foo")

    @patch.object(jcapiv1.SystemusersApi, 'systemusers_list')
    def test_get_user(self, mock_systemusers_list):
        users = [
            Systemuserreturn(**{
                'username': 'fake_user',
                'id': '1234',
                'firstname': 'Steve'
            }),
            Systemuserreturn(**{
                'username': 'fake_user_two',
                'id': '4321',
                'firstname': 'Angela'
            })
        ]
        response = Systemuserslist(results=users, total_count=len(users))
        mock_systemusers_list.return_value = response
        api1 = JumpcloudApiV1("fake_key")
        firstname = api1.get_user(username='fake_user')['firstname']
        assert (
            firstname == 'Steve'
        ), "Failed to retrieve correct user object"

    @patch.object(jcapiv1.SystemusersApi, 'systemusers_list')
    def test_get_user_no_id(self, mock_systemusers_list):
        users = [
            Systemuserreturn(
                username='dave',
                firstname='David',
                email='david@david.net'
            ),
            Systemuserreturn(
                username='zekun',
                firstname='Zekun',
                email='zekun.wang@david.net'
            )
        ]
        mock_systemusers_list.return_value = Systemuserslist(results=users, total_count=len(users))
        api1 = JumpcloudApiV1("fake_key_123")
        with pytest.raises(SystemUserNotFoundError):
            api1.get_user('angela')

    @patch.object(jcapiv1.SearchApi, 'search_systemusers_post')
    def test_search_users_no_results(self, mock_search_systemusers_post):
        users = []
        mock_search_systemusers_post.return_value = Systemuserslist(results=users, total_count=len(users))

        api1 = JumpcloudApiV1("fake_key_123")
        user_search = api1.search_users({'firstname': 'David'})
        assert (user_search == [])

        call_args, call_kwargs = mock_search_systemusers_post.call_args
        assert (call_kwargs['body']['filter'] == {'and': [{'firstname': 'David'}]})

    @patch.object(jcapiv1.SearchApi, 'search_systemusers_post')
    def test_search_users_no_field(self, mock_search_systemusers_post):
        users = [
            Systemuserreturn(
                username='dave',
                firstname='David',
                email='david@david.net'
            ),
        ]
        mock_search_systemusers_post.return_value = Systemuserslist(results=users, total_count=len(users))

        api1 = JumpcloudApiV1("fake_key_123")
        user_search = api1.search_users()
        assert (
                user_search == [user.to_dict() for user in users]
        )

        call_args, call_kwargs = mock_search_systemusers_post.call_args
        assert (
                call_kwargs['body']['filter'] == None
        )

    @patch.object(jcapiv1.SearchApi, 'search_systemusers_post')
    def test_search_users_single_field(self, mock_search_systemusers_post):
        users = [
            Systemuserreturn(
                username='dave',
                firstname='David',
                email='david@david.net'
            ),
        ]
        mock_search_systemusers_post.return_value = Systemuserslist(results=users, total_count=len(users))

        api1 = JumpcloudApiV1("fake_key_123")
        user_search = api1.search_users({'firstname': 'David'})
        assert (
            user_search == [user.to_dict() for user in users]
        )

        call_args, call_kwargs = mock_search_systemusers_post.call_args
        assert (
            call_kwargs['body']['filter'] == {'and': [{'firstname': 'David'}]}
        )

    @patch.object(jcapiv1.SearchApi, 'search_systemusers_post')
    def test_search_users_multi_field(self, mock_search_systemusers_post):
        users = [
            Systemuserreturn(
                username='dave',
                firstname='David',
                lastname='Smith',
                email='david@david.net'
            ),
        ]
        mock_search_systemusers_post.return_value = Systemuserslist(results=users, total_count=len(users))

        api1 = JumpcloudApiV1("fake_key_123")
        user_search = api1.search_users({'firstname': 'David', 'lastname': 'Smith'})
        assert (
                user_search == [user.to_dict() for user in users]
        )

        call_args, call_kwargs = mock_search_systemusers_post.call_args
        assert (
                call_kwargs['body']['filter'] == {'and': [{'firstname': 'David'}, {'lastname': 'Smith'}]}
        )

    @patch.object(jcapiv1.SystemusersApi, 'systemusers_put')
    @patch.object(JumpcloudApiV1, 'get_user_id')
    def test_set_user(self, mock_get_user_id, mock_systemusers_put):
        mock_get_user_id.return_value = '1234'
        user = Systemuserreturn(**{
            'email': 'updated_fake_email123@fake.com',
            'firstname': 'JC',
            'id': '5ee14bae31771d77fbd4c0e0',
            'lastname': 'Tester3',
            'username': 'jctester4'
        })
        mock_systemusers_put.return_value = user
        api1 = JumpcloudApiV1("fake_key_123")
        api_response = api1.set_user("fake_user", {'email': 'updated_fake_email@fakesite.com'})
        assert (
            api_response == user.to_dict()
        ), "set_user did not correctly call the systemusers_put API method"

    @patch.object(JumpcloudApiV1, 'search_users')
    def test_set_user_no_id(self, mock_systemusers_search):
        mock_systemusers_search.return_value = [
            {
                'firstname': 'Mary',
                'username': 'mary',
                'email': 'mary@google.microsoft'
            }
        ]
        api1 = JumpcloudApiV1("1234")
        with pytest.raises(SystemUserNotFoundError):
            api1.set_user(username='foo', attributes={'email': 'new_email@site.com'})

    @patch.object(jcapiv1.SystemusersApi,'systemusers_delete')
    @patch.object(JumpcloudApiV1,'get_user_id')
    def test_delete_user(self, mock_get_user_id, mock_systemusers_delete):
        mock_get_user_id.return_value = "1234"
        api1 = JumpcloudApiV1("1234")
        api1.delete_user("foo")

    @patch.object(jcapiv1.SystemusersApi,'systemusers_delete')
    @patch.object(JumpcloudApiV1,'get_user_id')
    def test_delete_user_no_id(self, mock_get_user_id, mock_systemusers_delete):
        mock_get_user_id.return_value = None
        api1 = JumpcloudApiV1("1234")
        with pytest.raises(SystemUserNotFoundError):
            api1.delete_user("foo")
