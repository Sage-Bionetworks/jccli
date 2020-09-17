#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.cli
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>
"""
import logging
import sys
import click
import click_log
from .group import group
from .sync import sync
from .user import user
from ..__init__ import __version__
from ..config import load_config


LOGGER = logging.getLogger(__name__)
click_log.basic_config(LOGGER)


@click.group()
@click.option('--key', "-k", type=str, help='Jumpcloud API key (can also use environmental variable: JC_API_KEY)',
              envvar='JC_API_KEY')
@click.option('--profile', '-p', type=str, help='A user profile, as specified in the config file')
@click_log.simple_verbosity_option(LOGGER)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, key, profile):
    """
    Run jccli.
    """
    try:
        config = load_config(profile)
    except KeyError:
        sys.exit("no profile found named: %s" % (profile,))

    # Try to get key from CLI, then from config
    if key:
        key = key
    elif config.get('key', None):
        key = config['key']
    else:
        sys.exit("please provide API key in config file or as optional argument")

    ctx.obj = {
        'key': key,
        'logger': LOGGER
    }


cli.add_command(user)
cli.add_command(group)
cli.add_command(sync)
