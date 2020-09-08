import json
import sys
from logging import Logger

import click
from jcapiv2 import GroupType
from jcapiv2.rest import ApiException

from jccli.errors import SystemUserNotFoundError
from jccli.jc_api_v1 import JumpcloudApiV1
from jccli.jc_api_v2 import JumpcloudApiV2


@click.group()
@click.pass_context
def group(ctx):
    """
    Command set for groups
    """
    pass


@group.command('create')
@click.option('--name', "-n", required=True, type=str, help='Name of the group')
@click.option('--user', 'type', flag_value='user_group')
@click.option('--system', 'type', flag_value='system_group')
@click.pass_context
def create_group(ctx, name, type):
    """
    Create a group
    """
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger: Logger = ctx.obj.get('logger')
    if type is None:
        logger.error('groups must have a type (either "user" or "system")')
        sys.exit(1)
    try:
        api2.create_group(name, type)
    except ApiException:
        logger.error(f"API error (confirm that no group of type '{type}' and name '{name}' already exists)")
        sys.exit(1)
    click.echo(f"successfully created group: {name}")


@group.command('get')
@click.option('--name', '-n', required=True, type=str, help='Name of the group')
@click.option('--user', 'type', flag_value='user_group')
@click.option('--system', 'type', flag_value='system_group')
@click.pass_context
def get_group(ctx, name, type):
    """
    Get detail view of a group
    """
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    if type is None:
        logger.error('groups must have a type (either "user" or "system")')
        sys.exit(1)
    group = api2.get_group(group_name=name, group_type=type)
    if group is None:
        logger.error(f"no group found of type '{type}', name '{name}'")
        sys.exit(1)
    serialized_response = json.dumps(group)
    click.echo(f"{serialized_response}")


@group.command('list')
@click.option('--user', 'type', flag_value='user_group', help='Restrict to user groups only')
@click.option('--system', 'type', flag_value='system_group', help='Restrict to system groups only')
@click.pass_context
def list_groups(ctx, type):
    """
    List groups
    """
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger: Logger = ctx.obj.get('logger')
    response = api2.get_groups(type=type)
    serialized_response = json.dumps(response, indent=2)
    click.echo(f"{serialized_response}")


@group.command('delete')
@click.option('--name', "-n", required=True, type=str, help='Name of the group')
@click.option('--user', 'type', flag_value='user_group')
@click.option('--system', 'type', flag_value='system_group')
@click.pass_context
def delete_group(ctx, name, type):
    """
    Delete a group
    """
    logger = ctx.obj.get('logger')
    if type is None:
        logger.error('groups must have a type (either "user" or "system")')
        sys.exit(1)
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    group = api2.get_group(group_name=name, group_type=type)
    if group is None:
        logger.error(f"no group found of type '{type}', name '{name}'")
        sys.exit(1)
    api2.delete_group(group['id'], type)
    click.echo(f"successfully deleted group {name}")


@group.command('add-user')
@click.option('--name', "-n", required=True, type=str, help='name of the group')
@click.option('--username', '-u', required=True, type=str, help='username of user to be added')
@click.pass_context
def add_user(ctx, name, username):
    """
    Add a user to a JumpCloud 'user' group
    """
    logger = ctx.obj.get('logger')

    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    try:
        user_id = api1.get_user_id(username)
    except SystemUserNotFoundError:
        logger.error(f"user '{username}' not found")
        sys.exit(1)
    group = api2.get_group(group_name=name, group_type=GroupType.USER_GROUP)
    if group is None:
        logger.error(f"no user group named '{name}' could be found")
        sys.exit(1)
    try:
        api2.bind_user_to_group(user_id, group['id'])
    except ApiException:
        logger.error(f"API error (confirm that user {username} has not already been added to group {name}")
        sys.exit(1)
    click.echo(f"Successfully added user '{username}' to group '{name}'")


@group.command('list-users')
@click.option('--name', '-n', required=True, help='name of the group')
@click.pass_context
def list_users(ctx, name):
    """
    List users in a JumpCloud 'user' group
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    group = api2.get_group(group_name=name, group_type=GroupType.USER_GROUP)
    if group:
        group_id = group['id']
    else:
        logger.error(f"no user group found with name {name}")
        sys.exit(1)
    user_ids = api2.list_group_users(group_id=group_id)
    users = api1.retrieve_users(user_ids=user_ids)
    serialized_response = json.dumps(users, indent=2)
    click.echo(f"{serialized_response}")


@group.command('remove-user')
@click.option('--name', "-n", required=True, type=str, help='name of the group')
@click.option('--username', '-u', required=True, type=str, help='username of user to be added')
@click.pass_context
def remove_user(ctx, name, username):
    """
    Remove a user from a JumpCloud 'user' group
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    try:
        user_id = api1.get_user_id(username)
    except SystemUserNotFoundError:
        logger.error(f"user '{username}' not found")
        sys.exit(1)
    group = api2.get_group(group_name=name, group_type=GroupType.USER_GROUP)
    if group is None:
        logger.error(f"group '{name}' not found")
        sys.exit(1)
    try:
        api2.unbind_user_from_group(user_id, group['id'])
    except ApiException:
        logger.error(f"API exception (confirm that '{username}' is a member of group '{name}')")
        sys.exit(1)
    click.echo(f"Successfully removed user '{username}' from group '{name}'")
