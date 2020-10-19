import configparser
import os
from jccli.config import CONFIG_FILE_PATH


TESTING_PROFILE = 'jccli-dev-testing'

api_key = os.getenv('JC_API_KEY')

if not api_key:
    # Do not allow the API in the [DEFAULT] section of config file to be used
    config = configparser.ConfigParser(default_section=None)
    config.read([CONFIG_FILE_PATH])
    api_key = config['jccli-dev-testing'].get('key')

API_KEY = api_key


def setup_module(module):
    assert API_KEY, \
        "Either `JC_API_KEY` environment variable or `key` in the jccli.ini [jccli-dev-testing] section is required"
