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
        configuration.api_key['x-api-key'] = api_key
        cls.systemusers_api = SystemusersApi(ApiClient(configuration=configuration))
        cls.api_key = api_key

        current_users: Systemuserslist = cls.systemusers_api.systemusers_list(
            content_type='application/json',
            accept='application/json'
        )
        assert current_users.total_count == 0

    def test_create_user(self):
        USERNAME = 'fakeuser567'
        EMAIL = 'fakeemail3@fakesite.org'

        runner = CliRunner()

        result = runner.invoke(cli.cli, [
            '--key',
            self.api_key,
            'user',
            'create',
            '--username',
            USERNAME,
            '--email',
            EMAIL
        ])
        if result.exit_code:
            raise ValueError(
                "create-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )

        generated_id = json.loads(result.output)['id']

        # Use API to delete created user
        self.systemusers_api.systemusers_delete(
            accept='application/json',
            content_type='application/json',
            id=generated_id
        )

    def test_delete_user(self):
        USERNAME = 'fakeuser789'
        EMAIL = 'fakeemail4@fakesite.org'

        # Create user to be deleted:
        self.systemusers_api.systemusers_post(
            content_type='application/json',
            accept='application/json',
            body=Systemuserputpost(
                username=USERNAME,
                email=EMAIL
            )
        )

        runner = CliRunner()

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
        # TODO: what output should we expect from delete-user

    def test_set_user(self):
        USERNAME = 'fakeuser987'
        FIRST_EMAIL = 'fakeemail@fakesite.edu'
        SECOND_EMAIL = 'fakeemail2@fakesite.edu'

        # Create user to be changed
        self.systemusers_api.systemusers_post(
            content_type='application/json',
            accept='application/json',
            body=Systemuserputpost(
                username=USERNAME,
                email=FIRST_EMAIL
            )
        )

        runner = CliRunner()

        # Set (update) a user using CLI
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
                "get-user exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            username = parsed_output['username']
            user_id = parsed_output['id']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert username == USERNAME, result.output

        # Check that the email was actually changed
        user = self.systemusers_api.systemusers_get(
            content_type='application/json',
            accept='application/json',
            id=user_id
        )
        assert user.email == SECOND_EMAIL

        # Delete the user
        self.systemusers_api.systemusers_delete(
            accept='application/json',
            content_type='application/json',
            id=user_id
        )
