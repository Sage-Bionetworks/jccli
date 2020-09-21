import os
import configparser
from pathlib import Path


DEFAULT_SECTION = 'DEFAULT'
CONFIG_FILE_PATH = str(Path.home().joinpath('.jccli.ini'))
CONFIG_DEFAULTS = {'key': ''}


def make_default_config():
    """Create a config file filled with default values. Only call this if no config file exists, or to overwrite it if
    it does.
    """
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        config = configparser.ConfigParser()
        config[DEFAULT_SECTION] = CONFIG_DEFAULTS
        config.write(config_file)


def load_config(profile=None):
    """Load profile from config file

    If profile is falsy, will load DEFAULT profile
    """
    # Create the configuration directory or the configuration file if either doesn't exist
    if not os.path.exists(CONFIG_FILE_PATH):
        make_default_config()

    if not profile:
        profile = DEFAULT_SECTION

    config = configparser.ConfigParser()
    config.read([CONFIG_FILE_PATH])
    return config[profile]
