import os
import sys
import configparser
from pathlib import Path


DEFAULT_SECTION = 'DEFAULT'
CONFIG_FILE_PATH = str(Path.home().joinpath('.jccli.ini'))
CONFIG_DEFAULTS = {}


def load_config(profile=DEFAULT_SECTION):
    """Load profile from config file

    If profile is falsy, will load DEFAULT profile. If no config file exists at ~/.jccli.ini, pretend there is one with
    default values.
    """
    # Create the configuration directory or the configuration file if either doesn't exist
    if not os.path.exists(CONFIG_FILE_PATH):
        if profile == DEFAULT_SECTION:
            return CONFIG_DEFAULTS.copy()
        else:
            sys.exit("No file found at '%s'. Cannot load profile: '%s'" % (CONFIG_FILE_PATH, profile))

    config = configparser.ConfigParser()
    config.read([CONFIG_FILE_PATH])
    if profile not in config:
        sys.exit("Profile '%s' not found in config file '%s'" % (profile, CONFIG_FILE_PATH))
    return config[profile]
