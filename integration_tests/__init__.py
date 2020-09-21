import configparser
import os


def setup_module(module):
    api_key = os.getenv('JC_API_KEY')
    assert (api_key is not None), \
        "The environmental variable `JC_API_KEY` must contain a valid Jumpcloud API key"

    # Change home dir to the integration_tests or project directory (doesn't really matter which) so that the config
    # file for testing purposes doesn't overwrite the dev's actual config file
    assert os.path.normpath(os.getenv('HOME')) == os.path.normpath(os.getcwd()) or os.getenv("TRAVIS"), \
        "The environmental variable `HOME` must be set to the project directory, unless this test is running on Travis"
    os.makedirs('.jccli')
    with open('.jccli/config.ini', 'w') as config_file:
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'key': api_key}
        config.write(config_file)


def teardown_module(module):
    os.remove('.jccli/config.ini')
    os.removedirs('.jccli')
