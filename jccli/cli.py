#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.cli
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>
"""
import logging
import click
import click_log
import jccli.helpers as jccli_helpers

from jccli.errors import MissingRequiredArgumentError
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
        user = jccli_helpers.get_user_from_term(json)
    elif file is not None:
        user = jccli_helpers.get_user_from_file(file)
    else:
        raise MissingRequiredArgumentError("SystemUser properties not provided")

    response = api1.create_user(user)
    LOGGER.info(f"{response}")

# @cli.command()
# @click.option('--username', "-u", required=True, type=str, help='The user name')
# @click.pass_context
# def delete_user(ctx, username):
#     """
#     Delete a jumpcloud user
#     """
#     api1 = JumpcloudApiV1(ctx.obj.get('key'))
#     user_id = api1.get_user_id(username)
#     if user_id is None:
#         raise SystemUserNotFoundError(f"System user {username} not found")
#
#     response = api1.delete_user(user_id)
#     LOGGER.info(f"{response}")

@cli.command()
@click.option('--username', "-u", required=True, type=str, help='The user name')
@click.pass_context
def delete_user(ctx, username):
    """
    Delete a jumpcloud user
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    response = api1.delete_user(username=username)
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
              prompt='Do you want to continue?',
              help='Assume yes to all questions')
@click.option('--dry-run', is_flag=True,
              help='Do not do anything, only show what will happen')
@click.pass_context
def sync(ctx, dry_run, data):
    # pylint: disable-msg=too-many-locals
    # pylint: disable-msg=too-many-branches
    """
    Sync Jumpcloud with a data file
    """
    if dry_run:
        LOGGER.setLevel(logging.DEBUG)

    LOGGER.debug("--- sync groups ----")
    groups = jccli_helpers.get_groups_from_file(data)
    sync_groups(ctx, groups)
    LOGGER.debug("--- sync users ----")
    users = jccli_helpers.get_users_from_file(data)
    sync_users(ctx, users)

def sync_groups(ctx, groups):
    # pylint: disable-msg=too-many-locals
    # pylint: disable-msg=too-many-branches
    """
    Sync Jumpcloud groups with definition in data file
    :param ctx: Click context
    :param groups: groups from data file
    :return:
    """
    key = ctx.obj.get('key')
    dry_run = ctx.params.get('dry_run')

    local_groups = groups

    api2 = JumpcloudApiV2(key)
    jc_group_names = []
    jc_groups_request = api2.get_groups()
    if jc_groups_request:
        for jc_group in jc_groups_request:
            jc_group_names.append(jc_group['_name'])

    LOGGER.debug(f"jumpcloud groups: {jc_group_names}")

    # create new groups
    added_groups = []
    for group in local_groups:
        do_create_group = False
        try:
            group_name = group['name']
            group_type = group['type']
            if group_name not in jc_group_names:
                do_create_group = True
            else:
                LOGGER.debug(f"{group_name} group already exists")
        except KeyError as error:
            raise error

        if do_create_group:
            added_groups.append(group_name)
            new_group = {}
            new_group['name'] = group_name
            new_group['type'] = group_type
            LOGGER.info(f"create {' '.join(group_type.split('_'))}: {group_name}")
            if not dry_run:
                response = api2.create_group(group_name, group_type)

    # remove groups that do not exist in the users file
    local_group_names = []
    for group in local_groups:
        local_group_names.append(group['name'])

    removed_groups = []
    for jc_group in jc_groups_request:
        jc_group_type = jc_group['_type']
        jc_group_name = jc_group['_name']
        do_remove_group = False
        if jc_group_name not in local_group_names:
            do_remove_group = True

        if do_remove_group:
            removed_groups.append(jc_group)
            LOGGER.info(f"remove {' '.join(jc_group_type.split('_'))}: {jc_group_name}")
            if not dry_run:
                response = api2.delete_group(jc_group_name)

def sync_users(ctx, users):
    # pylint: disable-msg=too-many-locals
    # pylint: disable-msg=too-many-branches
    # pylint: disable-msg=too-many-statements
    """
    Sync Jumpcloud users with definition in data file
    :param ctx: Click context
    :param users: users from data file
    :return:
    """
    local_users = users
    key = ctx.obj.get('key')
    dry_run = ctx.params.get('dry_run')

    api1 = JumpcloudApiV1(key)
    jc_usernames = []
    jc_emails = []
    jc_users = []
    jc_users_request = api1.get_users()
    if jc_users_request:
        for jc_user in jc_users_request:
            jc_usernames.append(jc_user['_username'])
            jc_emails.append(jc_user['_email'])
            jc_users.append({'username': jc_user['_username'], 'email': jc_user['_email']})

    LOGGER.debug(f"jumpcloud users: {jc_usernames}")

    # create new users
    api2 = JumpcloudApiV2(key)
    added_users = []
    for user in local_users:
        do_create_user = False
        try:
            user_name = user['username']
            user_email = user['email']
            if (user_name not in jc_usernames) and (user_email not in jc_emails):
                do_create_user = True
            else:
                LOGGER.debug(f"{user_name} user already exists")
        except KeyError as error:
            raise error

        if do_create_user:
            added_users.append({'username': user_name, 'email': user_email})
            new_user = {}
            new_user['username'] = user_name
            new_user['email'] = user_email
            new_user['firstname'] = user['firstname']
            new_user['firstname'] = user['lastname']
            LOGGER.info(f"create user: {user_name}")
            if not dry_run:
                response = api1.create_user(new_user)
                group_id, group_type = api2.get_group("staff")
                if group_id:
                    user_id = api1.get_user_id(user_name)
                    LOGGER.info(f"bind {user_id} to group: {group_id}")
                    if not dry_run:
                        api2.bind_user_to_group(user_id, group_id)

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
            removed_users.append(jc_user)
            LOGGER.info(f"remove user: {user_name}")
            if not dry_run:
                response = api1.delete_user(username=user_name)
