import os


TESTING_PROFILE = 'jccli-dev-testing'


def setup_module(module):
    api_key = os.getenv('JC_API_KEY')
    assert (api_key is not None), \
        "The environmental variable `JC_API_KEY` must contain a valid Jumpcloud API key"
