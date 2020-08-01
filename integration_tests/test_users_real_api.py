import json
import os

from jcapiv1 import ApiClient, Configuration, Systemuserslist, Systemuserputpost

from jccli import cli
from click.testing import CliRunner, Result
from jcapiv1.api.systemusers_api import SystemusersApi


class TestUsersRealApi:
    @classmethod
    def setup_class(cls):
        configuration = Configuration()
        api_key = os.getenv('JC_API_KEY')
        assert (api_key is not None),\
            "The environmental variable `JC_API_KEY` must contain a valid Jumpcloud API key"
        configuration.api_key['x-api-key'] = api_key
        cls.systemusers_api = SystemusersApi(ApiClient(configuration=configuration))
        cls.api_key = api_key

        current_users: Systemuserslist = cls.systemusers_api.systemusers_list(
            content_type='application/json',
            accept='application/json'
        )
        assert current_users.total_count == 0

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
                "create-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            username = parsed_output['username']
            email = parsed_output['email']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert username == USERNAME, result.output
        assert email == FIRST_EMAIL, result.output

        # Set (update) the user
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'set',
            '--username',
            USERNAME,
            '--email',
            SECOND_EMAIL
        ])
        if result.exit_code:
            raise ValueError(
                "set-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            username = parsed_output['username']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert username == USERNAME, result.output

        # Get the user
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
                "get-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            username = parsed_output['username']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert username == USERNAME, result.output

        # Delete the user
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'delete',
            '--username',
            USERNAME
        ])
        assert result.output == ''

    def test_multi_user(self):
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
                '--key',
                self.api_key,
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

        # Get a list of all users
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'list'
        ])
        if result.exit_code:
            raise ValueError(
                "list-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        firstnames = [user['firstname'] for user in parsed_output]
        lastnames = [user['lastname'] for user in parsed_output]
        print("First & Last Names:")
        print(firstnames)
        print(lastnames)
        print("Parsed Output:")
        print(parsed_output)
        assert all(firstname in firstnames for firstname in ('David', 'Ahamed'))
        assert all(lastname in lastnames for lastname in ('Smith', 'Weinberg'))
        assert len(parsed_output) == 3

        # Search for users with a particular last name
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'list',
            '--lastname',
            'Weinberg'
        ])
        if result.exit_code:
            raise ValueError(
                "list-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        firstnames = [user['firstname'] for user in parsed_output]
        lastnames = [user['lastname'] for user in parsed_output]
        assert all(firstname in firstnames for firstname in ('David', 'Ahamed'))
        assert all(lastname == 'Weinberg' for lastname in lastnames)
        assert len(parsed_output) == 2

        # Search for users with a particular last & first name
        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'list',
            '--firstname',
            'Ahamed',
            '--lastname',
            'Weinberg'
        ])
        if result.exit_code:
            raise ValueError(
                "list-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert parsed_output[0]['firstname'] == 'Ahamed'
        assert parsed_output[0]['lastname'] == 'Weinberg'
        assert len(parsed_output) == 1

        # Clean up. Delete the users
        for user in USERS:
            result = runner.invoke(cli.cli, [
                '--key',
                self.api_key,
                'user',
                'delete',
                '--username',
                user['username']
            ])
            if result.exit_code:
                raise ValueError(
                    "delete-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
                )
