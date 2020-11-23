import json
import time

import docker
import jcapiv1
import os

from click.testing import CliRunner
from jcapiv1 import SystemsApi
from integration_tests import API_KEY
from jccli import cli


JC_CONNECT_KEY = os.getenv('JC_CONNECT_KEY')
DOCKER_IMAGE = 'sagejcdevs/jumpcloud-agent:v0.0.2'  # Name of image to spin up
SYSTEM_COUNT = 5  # The number of docker containers to spin up and connect to the cloud


class TestSystemsRealApi:
    @classmethod
    def setup_class(cls):
        '''
        Spin up docker images and check that they have connected
        '''

        apiv1_configuration = jcapiv1.Configuration()
        apiv1_configuration.api_key['x-api-key'] = API_KEY
        cls.systems_api = SystemsApi(jcapiv1.ApiClient(configuration=apiv1_configuration))

        current_systems = cls.systems_api.systems_list(
            content_type='application_json',
            accept='application/json'
        )
        assert current_systems.total_count == 0

        docker_client = docker.from_env()
        cls.containers = []
        for i in range(SYSTEM_COUNT):
            container = docker_client.containers.run(
                DOCKER_IMAGE,
                environment={'JC_CONNECT_KEY': JC_CONNECT_KEY},
                detach=True,
                stdin_open=True,
                tty=True
            )
            cls.containers.append(container)

        # Wait for containers to boot up and connect to JumpCloud
        # Cycle for a maximum of 10 minutes
        for i in range(600):
            time.sleep(1)
            current_systems = cls.systems_api.systems_list(
                content_type='application/json',
                accept='application/json'
            )
            print("number of reporting systems on JumpCloud:")
            print(current_systems.total_count)
            if current_systems.total_count == SYSTEM_COUNT:
                break

        # Check whether system hostnames have loaded (this takes a while after they phone home)
        # Cycle for a maximum of 10 minutes
        for i in range(600):
            time.sleep(1)
            print("checking whether hostnames have loaded for docker containers")
            current_systems = cls.systems_api.systems_list(
                content_type='application/json',
                accept='application/json'
            )
            if current_systems.results[0].hostname:
                break

    def test_delete_system(self):
        runner = CliRunner()

        # Pick a system's id from listed systems
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'list'
        ])
        if result.exit_code:
            raise ValueError(
                "list-systems exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            system_id = parsed_output[0]['id']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)

        # Delete first host
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'delete',
            '--id',
            system_id
        ])
        if result.exit_code:
            raise ValueError(
                "delete-system exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )

        # Check number of hosts remaining
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'list',
        ])
        if result.exit_code:
            raise ValueError(
                "list-systems exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            connected_systems = len(parsed_output)
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)

        assert connected_systems == SYSTEM_COUNT - 1, "System was not successfully deleted"

    def test_list_systems(self):
        runner = CliRunner()

        # Pick a system's hostname and os from listed systems
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'list'
        ])
        if result.exit_code:
            raise ValueError(
                "list-systems exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            systems_count = len(parsed_output)
            system = parsed_output[0]
            system_id = system['id']
            hostname = system['hostname']
            display_name = system['display_name']
            architecture = system['arch']
            operating_system = system['os']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)

        # List systems only matching os and architecture of original system
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'list',
            '--os',
            operating_system,
            '--arch',
            architecture
        ])
        if result.exit_code:
            raise ValueError(
                "list-systems exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            for system in parsed_output:
                assert system['arch'] == architecture
                assert system['os'] == operating_system
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)

        # List systems only matching hostname
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'list',
            '--hostname',
            hostname,
        ])
        if result.exit_code:
            raise ValueError(
                "list-systems exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            assert len(parsed_output) == 1  # Only one system should have the same hostname in our test suite
            system = parsed_output[0]
            assert system['hostname'] == hostname
            assert system['id'] == system_id  # It should be the exact same system
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)

    def test_update_system(self):
        DISPLAY_NAME = 'computer-number-one'
        runner = CliRunner()

        # List systems, pick the first one
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'list'
        ])
        if result.exit_code:
            raise ValueError(
                "list-systems exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            system_id = parsed_output[0]['id']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)

        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'set',
            '--id',
            system_id,
            '--display-name',
            DISPLAY_NAME,
            '--allow-ssh-password-authentication'
        ])
        if result.exit_code:
            raise ValueError(
                "set-system exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )

        # Check that the system was changed successfully
        result = runner.invoke(cli.cli, [
            '--key',
            API_KEY,
            'system',
            'get',
            '--id',
            system_id
        ])
        if result.exit_code:
            raise ValueError(
                "list-systems exited with status code: %s;\nmessage was: %s" % (result.exit_code, result.exception)
            )
        try:
            parsed_output = json.loads(result.output)
            allow_ssh_authentication = parsed_output['allow_ssh_password_authentication']
            display_name = parsed_output['display_name']
        except json.decoder.JSONDecodeError:
            raise ValueError(result.output)
        assert allow_ssh_authentication
        assert display_name == DISPLAY_NAME

    @classmethod
    def teardown_class(cls):
        # Delete remaining systems from JC
        api_response = cls.systems_api.systems_list(
            accept='application/json',
            content_type='application/json'
        )
        for system in api_response.results:
            cls.systems_api.systems_delete(
                accept='application/json',
                content_type='application/json',
                id=system.id
            )

        # Stop containers
        for container in cls.containers:
            container.stop()
