import json
import os
from jccli import cli
from click.testing import CliRunner, Result


class TestRealApi:
    @classmethod
    def setup_class(cls):
        cls.api_key = os.getenv('JC_API_KEY')

    def test_no_users(self):
        """Check to see if the system corresponding to our API key is clean. No other tests are likely to pass if this
        one is failing.
        """

    def test_create_and_delete(self):
        USERNAME = 'fakeuser567'
        EMAIL = 'fakeemail3@fakesite.org'

        runner = CliRunner()

        runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'create',
            '--username',
            USERNAME,
            '--email',
            EMAIL
        ])

        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'get',
            '--username',
            USERNAME
        ])
        if result.exit_code:
            raise ValueError(
                "get-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception))
        try:
            user = json.loads(result.output)
            username = user['username']
            email = user['email']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert username == USERNAME, result.output
        assert email == EMAIL, result.output

        runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'delete',
            '--username',
            USERNAME
        ])


    def test_single_user(self):
        USERNAME = 'fakeuser987'
        FIRST_EMAIL = 'fakeemail@fakesite.edu'
        SECOND_EMAIL = 'fakeemail2@fakesite.edu'

        runner = CliRunner()

        # Create a user
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'create',
            '--username',
            USERNAME,
            '--email',
            FIRST_EMAIL
        ])
        if result.exit_code:
            raise ValueError(
                "get-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception))
        try:
            username = json.loads(result.output)['username']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert username == USERNAME, result.output

        # Get detail view of created user
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'get',
            '--username',
            USERNAME
        ])
        if result.exit_code:
            raise ValueError(
                "get-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception))
        try:
            email = json.loads(result.output)['email']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert email == FIRST_EMAIL, result.output

        # Update user's email address
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'set',
            '--username',
            'fakeuser987',
            '--email',
            SECOND_EMAIL
        ])
        if result.exit_code:
            raise ValueError(
                "get-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception))
        try:
            email = json.loads(result.output)['email']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert email == SECOND_EMAIL, result.output

        # Double check that the email address was updated
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'get',
            '--username',
            USERNAME
        ])
        if result.exit_code:
            raise ValueError(
                "get-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception))
        try:
            email = json.loads(result.output)['email']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert email == SECOND_EMAIL, result.output

        # Delete the user
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'delete',
            '--username',
            USERNAME
        ])
        if result.exit_code:
            raise ValueError(
                "get-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception))
