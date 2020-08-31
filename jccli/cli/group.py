import json
import sys
from logging import Logger

import click
from jcapiv2 import GroupType

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
    response = api2.create_group(name, type)
    logger.info(f"successfully created group: {name}")


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
    response = api2.get_group(group_name=name, group_type=type)
    serialized_response = json.dumps(response)
    logger.info(f"{serialized_response}")


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
    logger.info(f"{serialized_response}")


@group.command('delete')
@click.option('--name', "-n", required=True, type=str, help='Name of the group')
@click.option('--user', 'type', flag_value='user_group')
@click.option('--system', 'type', flag_value='system_group')
@click.pass_context
def delete_group(ctx, name, type):
    """
    Delete a group
    """
    # FIXME: Ideally, this would output JSON info of the deleted group (similar to delete-user), but at the moment it's
    #  unclear exactly how to do that, given the API wrappers that we have.
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    api2.delete_group(name, type)
    logger.info(f"successfully deleted group {name}")


@group.command('add-user')
@click.option('--name', "-n", required=True, type=str, help='name of the group')
@click.option('--username', '-u', required=True, type=str, help='username of user to be added')
@click.pass_context
def add_user(ctx, name, username):
    """
    Add user to group (group type is assumed to be 'user_group')
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    user_id = api1.get_user(username)['id']
    group_id = api2.get_group(group_name=name, group_type=GroupType.USER_GROUP)['id']
    result = api2.bind_user_to_group(user_id, group_id)
    logger.info(f"{result}")


@group.command('list-users')
@click.option('--name', '-n', required=True, help='name of the group')
@click.pass_context
def list_users(ctx, name):
    """
    List users in a group (group type is assumed to be 'user_group')
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
    logger.info(f"{serialized_response}")


@group.command('remove-user')
@click.option('--name', "-n", required=True, type=str, help='name of the group')
@click.option('--username', '-u', required=True, type=str, help='username of user to be added')
@click.pass_context
def remove_user(ctx, name, username):
    """
    Remove user from group (group type is assumed to be 'user_group')
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    user_id = api1.get_user(username)['id']
    group_id = api2.get_group(group_name=name, group_type=GroupType.USER_GROUP)['id']
    result = api2.unbind_user_from_group(user_id, group_id)
    logger.info(f"{result}")
