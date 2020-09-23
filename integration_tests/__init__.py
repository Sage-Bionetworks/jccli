import configparser
import os


def setup_module(module):
    api_key = os.getenv('JC_API_KEY')
    assert (api_key is not None), \
        "The environmental variable `JC_API_KEY` must contain a valid Jumpcloud API key"

    # Check that HOME is set to the project directory, ensuring that running the tests won't accidentally overwrite
    # their own ~/.jccli.ini file.
    assert os.path.basename(os.path.normpath(os.getenv('HOME'))) == 'jccli' or os.getenv("TRAVIS"), \
        "The environmental variable `HOME` must be set to the project directory, unless this test is running on Travis"
    with open('.jccli.ini', 'w') as config_file:
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'key': api_key}
        config.write(config_file)


def teardown_module(module):
    os.remove('.jccli.ini')
