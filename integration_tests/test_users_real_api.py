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
