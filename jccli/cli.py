#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.cli
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>
"""
import logging
import click
import click_log


from jccli.errors import SystemUserNotFoundError, MissingRequiredArgumentError
from jccli.helpers import get_users_from_file, get_user_from_file, get_user_from_term
from jccli.helpers import get_groups_from_file
from jccli.jc_api_v1 import JumpcloudApiV1
from jccli.jc_api_v2 import JumpcloudApiV2
from .__init__ import __version__

# setup click-log
LOGGER = logging.getLogger(__name__)
click_log.basic_config(LOGGER)

def abort_if_false(ctx, param, value):
    # pylint: disable=unused-argument
    """
    A click handler for user prompts
    """
    if not value:
        ctx.abort()

@click.group()
@click.option('--key', "-k", required=False, type=str, help='Jumpcloud API key')
@click_log.simple_verbosity_option(LOGGER)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, key):
    """
    Run jccli.
    """
    ctx.obj = {
        'key': key
    }

@cli.command()
@click.option('--json', "-j", required=False, type=str,
              help='SystemUser properties json')
@click.option('--file', "-f", required=False, type=click.Path(exists=True),
              help='SystemUser properties file')
@click.pass_context
def create_user(ctx, json, file):
    """
    Create a new Jumpcloud user
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    user = {}
    if json is not None:
        user = get_user_from_term(json)
    elif file is not None:
        user = get_user_from_file(file)
    else:
        raise MissingRequiredArgumentError("SystemUser properties not provided")

    response = api1.create_user(user)
    LOGGER.info(f"{response}")

@cli.command()
@click.option('--username', "-u", required=True, type=str, help='The user name')
@click.pass_context
def delete_user(ctx, username):
    """
    Delete a jumpcloud user
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    user_id = api1.get_user_id(username)
    if user_id is None:
        raise SystemUserNotFoundError(f"System user {username} not found")

    response = api1.delete_user(user_id)
    LOGGER.info(f"{response}")

@cli.command()
@click.option('--name', "-n", required=True, type=str, help='Name of the group')
@click.option('--type', "-t", required=True, type=click.Choice(['user', 'system']),
              help='The type of group')
@click.pass_context
def create_group(ctx, name, type):
    """
    Create a Jumpcloud group
    """
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    response = api2.create_group(name, type)
    LOGGER.info(f"{response}")

@cli.command()
@click.option('--name', "-n", required=True, type=str, help='Name of the group')
@click.pass_context
def delete_group(ctx, name):
    """
    Delete a Jumpcloud group
    """
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    api2.delete_group(name)
    LOGGER.info(f"Group {name} deleted")

@cli.command()
@click.option('--data', "-d", required=True, type=click.Path(exists=True),
              help='The JC data file')
@click.option('--yes', "-y", is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure?')
@click.pass_context
def sync(ctx, data):
    # pylint: disable-msg=too-many-locals
    # pylint: disable-msg=too-many-branches
    """
    Sync Jumpcloud with a data file
    """
    key = ctx.obj.get('key')
    users = get_users_from_file(data)
    groups = get_groups_from_file(data)

    api1 = JumpcloudApiV1(key)
    jc_usernames = []
    jc_emails = []
    jc_users = []
    jc_users_request = api1.get_users(limit='')
    if jc_users_request:
        for jc_user in jc_users_request:
            jc_usernames.append(jc_user['_username'])
            jc_emails.append(jc_user['_email'])
            jc_users.append({'username':jc_user['_username'], 'email':jc_user['_email']})

    LOGGER.info(f"jumpcloud users: {jc_usernames}")

    # create new users
    api2 = JumpcloudApiV2(key)
    added_users = []
    for user in users:
        do_create_user = False
        try:
            user_name = user['username']
            user_email = user['email']
            if (user_name not in jc_usernames) and (user_email not in jc_emails):
                do_create_user = True
            else:
                LOGGER.info(f"{user_name} user already exists")
        except KeyError as error:
            raise error

        if do_create_user:
            LOGGER.info(f"creating user: {user_name}")
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
                LOGGER.info(f"binding {user_id} to group: {group_id}")
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
            LOGGER.info(f"removing user: {user_name}")
            removed_users.append(jc_user)
