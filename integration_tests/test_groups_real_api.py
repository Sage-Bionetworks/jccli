import json
from click.testing import CliRunner
from integration_tests import API_KEY
from jccli import cli
import jcapiv1
import jcapiv2
from jcapiv1.api.systemusers_api import SystemusersApi
from jcapiv2.api.user_groups_api import UserGroupsApi


GROUP_NAME = 'fake-group-123'
USERS = [
    {
        'firstname': 'David',
        'lastname': 'Smith',
        'email': 'david.smith@fakesite.org',
        'username': 'david_smith_123'
    },
    {
        'firstname': 'David',
        'lastname': 'Weinberg',
        'email': 'david.weinberg@fakesite.org',
        'username': 'david_weinberg_456'
    },
    {
        'firstname': 'Ahamed',
        'lastname': 'Weinberg',
        'email': 'ahamed.weinberg@fakesite.org',
        'username': 'ahamed_weinberg_789'
    }
]


class TestGroupsRealApi:
    @classmethod
    def setup_class(cls):
        '''Check that there are no existing users, and no groups named 'fake-group-123' in JC test account
        '''
        apiv1_configuration = jcapiv1.Configuration()
        apiv1_configuration.api_key['x-api-key'] = API_KEY
        systemusers_api = SystemusersApi(jcapiv1.ApiClient(configuration=apiv1_configuration))

        current_users = systemusers_api.systemusers_list(
            content_type='application/json',
            accept='application/json'
        )
        assert current_users.total_count == 0

        apiv2_configuration = jcapiv2.Configuration()
        apiv2_configuration.api_key['x-api-key'] = API_KEY
        user_groups_api = UserGroupsApi(jcapiv2.ApiClient(configuration=apiv2_configuration))

        current_groups = user_groups_api.groups_user_list(
            content_type='application/json',
            accept='application/json'
        )
        assert not any(group.name == GROUP_NAME for group in current_groups), "no groups on the JumpCloud instance " \
                                                                              "can have the same name as the groups " \
                                                                              "used in this integration test"

    def test_user_group(self):

        runner = CliRunner()

        # Create some users
        for user in USERS:
            result = runner.invoke(cli.cli, [
                '--key',
                API_KEY,
                'user',
                'create',
                '--username',
                user['username'],
                '--email',
                user['email'],
                '--firstname',
                user['firstname'],
                '--lastname',
                user['lastname']
            ])
            if result.exit_code:
                raise ValueError(
                    "create-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
                )
            try:
                parsed_output = json.loads(result.output)
            except json.decoder.JSONDecodeError:
                raise ValueError(result.output)

        # Create group
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'group',
            'create',
            '--user',
            '--name',
            GROUP_NAME
        ])
        if result.exit_code:
            raise ValueError(
                "create-group exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )

        # Assign two users to group
        for user in USERS[:2]:
            result = runner.invoke(cli.cli, [
                '--key',
                API_KEY,
                'group',
                'add-user',
                '--username',
                user['username'],
                '--name',
                GROUP_NAME
            ])
            if result.exit_code:
                raise ValueError(
                    "add-user-to-group exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
                )

        # Check group membership
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'group',
            'list-users',
            '--name',
            GROUP_NAME
        ])
        if result.exit_code:
            raise ValueError(
                "list-users exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert USERS[0]['username'] in [user['username'] for user in parsed_output]
        assert USERS[1]['username'] in [user['username'] for user in parsed_output]

        # Unbind a user
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'group',
            'remove-user',
            '--name',
            GROUP_NAME,
            '--username',
            USERS[1]['username']
        ])
        if result.exit_code:
            raise ValueError(
                "remove-user-from-group exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )

        # Check user has been removed
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'group',
            'list-users',
            '--name',
            GROUP_NAME
        ])
        if result.exit_code:
            raise ValueError(
                "list-users exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert USERS[0]['username'] in [user['username'] for user in parsed_output]
        assert USERS[1]['username'] not in [user['username'] for user in parsed_output]

        # Clean up:
        # Delete the users
        for user in USERS:
            result = runner.invoke(cli.cli, [
                '--key',
                API_KEY,
                'user',
                'delete',
                '--username',
                user['username']
            ])
            if result.exit_code:
                raise ValueError(
                    "delete-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
                )

        # Delete the group
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'group',
            'delete',
            '--user',
            '--name',
            GROUP_NAME
        ])
        if result.exit_code:
            raise ValueError(
                "delete-group exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
