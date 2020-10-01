import json

from click.testing import CliRunner
from integration_tests import TESTING_PROFILE
from jccli import cli


class TestGroupsRealApi:
    def test_user_group(self):
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

        runner = CliRunner()

        # Create some users
        for user in USERS:
            result = runner.invoke(cli.cli, [
                '--profile',
                TESTING_PROFILE,
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
            '--profile',
            TESTING_PROFILE,
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
                '--profile',
                TESTING_PROFILE,
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
            '--profile',
            TESTING_PROFILE,
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
            '--profile',
            TESTING_PROFILE,
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
            '--profile',
            TESTING_PROFILE,
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
                '--profile',
                TESTING_PROFILE,
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
            '--profile',
            TESTING_PROFILE,
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
