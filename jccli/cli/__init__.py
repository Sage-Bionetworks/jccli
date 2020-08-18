#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.cli
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>
"""
import sys
import click
from .group import group
from .sync import sync
from .user import user
from ..__init__ import __version__


@click.group()
@click.option('--key', "-k", type=str, help='Jumpcloud API key (can also use environmental variable: JC_API_KEY)',
              envvar='JC_API_KEY')
@click.option('--key-file', '-K', type=str, help='Path to text file containing Jumpcloud API key')
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, key, key_file):
    """
    Run jccli.
    """
    if key and key_file:
        sys.exit("Please provide a key *or* a key file, not both")
    if key_file and not key:
        key = open(key_file).read()
    ctx.obj = {
        'key': key
    }


cli.add_command(user)
cli.add_command(group)
cli.add_command(sync)
