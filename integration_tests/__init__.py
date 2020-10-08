import configparser
import os
from pathlib import Path

TESTING_PROFILE = 'jccli-dev-testing'
CONFIG_FILE_PATH = str(Path.home().joinpath('.jccli.ini'))


def setup_module(module):
    api_key = os.getenv('JC_API_KEY')

    if not api_key:
        # Do not allow the API in the [DEFAULT] section of config file to be used
        config = configparser.ConfigParser(default_section=None)
        config.read([CONFIG_FILE_PATH])
        api_key = config['jccli-dev-testing'].get('key')

    assert (api_key is not None), \
        "Either a `JC_API_KEY` environment variable or a `key` in the jccli.ini [jccli-dev-testing] section is required"
