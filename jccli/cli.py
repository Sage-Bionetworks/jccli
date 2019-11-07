#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.cli
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is the entry point for the command-line interface (CLI) application.  It
can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.
"""
import logging
import click
from jccli.errors import SystemUserNotFoundError, MissingRequiredArgumentError

from jccli.helpers import get_users_from_file, get_user_from_file, get_user_from_term
from jccli.helpers import get_groups_from_file
from jccli.jc_api_v1 import JumpcloudApiV1
from jccli.jc_api_v2 import JumpcloudApiV2
from .__init__ import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info():
    """
    An information object to pass data between CLI functions.
    """

    def __init__(self):  # Note: This object must have an empty constructor.
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


@click.group()
@click.option('--key', "-k", required=False, type=str, help='Jumpcloud API key')
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info, key, verbose: int):
    """
    Run jccli.
    """
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose
    info.key = key

@cli.command()
def version():
    """
    Get the version.
    """
    click.echo(click.style(f"{__version__}", bold=True))


@cli.command()
@click.option('--json', "-j", required=False, type=str,
              help='SystemUser properties json')
@click.option('--file', "-f", required=False, type=click.Path(exists=True),
              help='SystemUser properties file')
@pass_info
def create_user(info, json, file):
    """
    Create a new Jumpcloud user
    """
    api1 = JumpcloudApiV1(info.key)
    user = {}
    if json is not None:
        user = get_user_from_term(json)
    elif file is not None:
        user = get_user_from_file(file)
    else:
        raise MissingRequiredArgumentError("SystemUser properties not provided")

    click.echo("Create jumpcloud user " + user['username'])
    response = api1.create_user(user)
    click.echo(response)

@cli.command()
@click.option('--name', "-n", required=True, type=str, help='Name of the group')
@click.option('--type', "-t", required=True, type=click.Choice(['user', 'system']),
              help='The type of group')
@pass_info
def create_group(info, name, type):
    """
    Create a Jumpcloud group
    """
    api2 = JumpcloudApiV2(info.key)
    # click.echo("Create jumpcloud {} group {}".format(type, name))
    response = api2.create_group(name, type)
    click.echo(
        click.style(
            f"{response}",
            fg="green",
        )
    )

@cli.command()
@click.option('--name', "-n", required=True, type=str, help='Name of the group')
@pass_info
def delete_group(info, name):
    """
    Delete a Jumpcloud group
    """
    api2 = JumpcloudApiV2(info.key)
    response = api2.delete_group(name)
    if response is None:
        click.echo("Jumpcloud group deleted")

@cli.command()
@click.option('--username', "-u", required=False, type=str, help='The user name')
@pass_info
def delete_user(info, username):
    """
    Delete a jumpcloud user
    """
    if username is None:
        raise MissingRequiredArgumentError("Deleting a user requires a username")

    api1 = JumpcloudApiV1(info.key)
    click.echo("Delete jumpcloud user " + username)
    id = api1.get_user_id(username)
    if id is None:
        raise SystemUserNotFoundError("System user {} not found".format(username))

    response = api1.delete_user(id)
    click.echo(response)


@cli.command()
@click.option('--data', "-d", required=True, type=click.Path(exists=True),
              help='The JC data file')
@pass_info
def sync(info, data):
    """
    Sync Jumpcloud with a data file
    """
    click.echo("Sync data on jumpcloud with data in " + data)
    users = get_users_from_file(data)
    groups = get_groups_from_file(data)
    if users is None:
        raise MissingRequiredArgumentError("A sync requires a config file")

    sync_users(info.key, users)


def sync_users(key, users):
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=too-many-branches
    """
    Sync data file with jumpcloud
    """
    api1 = JumpcloudApiV1(key)
    api2 = JumpcloudApiV2(key)

    jc_usernames = []
    jc_emails = []
    jc_users = []
    jc_users_request = api1.get_users(limit='')
    if jc_users_request:
        for jc_user in jc_users_request:
            jc_usernames.append(jc_user['_username'])
            jc_emails.append(jc_user['_email'])
            jc_users.append({'username':jc_user['_username'], 'email':jc_user['_email']})

    click.echo("jumpcloud users: " + ','.join(jc_usernames))

    # create new users
    added_users = []
    for user in users:
        do_create_user = False
        try:
            user_name = user['username']
            user_email = user['email']
            if (user_name not in jc_usernames) and (user_email not in jc_emails):
                do_create_user = True
            else:
                click.echo(user_name + " user already exists")
        except KeyError as e:
            raise e

        if do_create_user:
            click.echo("creating user: " + user_name)
            # response = api1.create_user(user_name,
            #                             user_email,
            #                             user['firstname'],
            #                             user['lastname'])
            # if response is not None:
            #     added_users.append({'username':user_name, 'email':user_email})
            added_users.append({'username':user_name, 'email':user_email})
            group_id = api2.get_group("staff")
            if group_id:
                user_id = api1.get_user_id(user_name)
                click.echo("binding " + user_id + " to group: " + group_id)
                # api2.bind_user_to_group(user_id, group_id)

    # remove users that do not exist in the users file
    local_usernames = []
    local_emails = []
    for user in users:
        local_usernames.append(user['username'])
        local_emails.append(user['email'])

    removed_users = []
    for jc_user in jc_users:
        do_remove_user = False
        user_name = jc_user['username']
        user_email = jc_user['email']
        if (user_name not in local_usernames) and (user_email not in local_emails):
            do_remove_user = True

        if do_remove_user:
            click.echo("removing user: " + user_name)
            removed_users.append(jc_user)
