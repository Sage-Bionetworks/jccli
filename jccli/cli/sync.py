import logging
import click

from jccli import helpers as jccli_helpers
from jccli.jc_api_v1 import JumpcloudApiV1
from jccli.jc_api_v2 import JumpcloudApiV2


def abort_if_false(ctx, param, value):
    # pylint: disable=unused-argument
    """
    A click handler for user prompts
    """
    if not value:
        ctx.abort()


@click.command()
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
    logger = ctx.obj.get('logger')

    if dry_run:
        logger.setLevel(logging.DEBUG)

    logger.debug("--- sync groups ----")
    groups = jccli_helpers.get_groups_from_file(data)
    sync_groups(ctx, groups)
    logger.debug("--- sync users ----")
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
    logger = ctx.obj.get('logger')
    dry_run = ctx.params.get('dry_run')

    local_groups = groups

    api2 = JumpcloudApiV2(key)
    jc_group_names = []
    jc_groups_request = api2.get_groups()
    if jc_groups_request:
        for jc_group in jc_groups_request:
            jc_group_names.append(jc_group['_name'])

    logger.debug(f"jumpcloud groups: {jc_group_names}")

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
                logger.debug(f"{group_name} group already exists")
        except KeyError as error:
            raise error

        if do_create_group:
            added_groups.append(group_name)
            new_group = {}
            new_group['name'] = group_name
            new_group['type'] = group_type
            click.echo(f"create {' '.join(group_type.split('_'))}: {group_name}")
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
            click.echo(f"remove {' '.join(jc_group_type.split('_'))}: {jc_group_name}")
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
    logger = ctx.obj.get('logger')
    dry_run = ctx.params.get('dry_run')

    api1 = JumpcloudApiV1(key)
    jc_usernames = []
    jc_emails = []
    jc_users = []
    jc_users_request = api1.get_users()
    if jc_users_request:
        for jc_user in jc_users_request:
            jc_usernames.append(jc_user['username'])
            jc_emails.append(jc_user['email'])
            jc_users.append({'username': jc_user['username'], 'email': jc_user['email']})

    logger.debug(f"jumpcloud users: {jc_usernames}")

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
                logger.debug(f"{user_name} user already exists")
        except KeyError as error:
            raise error

        if do_create_user:
            added_users.append({'username': user_name, 'email': user_email})
            new_user = {}
            new_user['username'] = user_name
            new_user['email'] = user_email
            new_user['firstname'] = user['firstname']
            new_user['firstname'] = user['lastname']
            click.echo(f"create user: {user_name}")
            if not dry_run:
                response = api1.create_user(new_user)
                group_id, group_type = api2.get_group("staff")
                if group_id:
                    user_id = api1.get_user_id(user_name)
                    click.echo(f"bind {user_id} to group: {group_id}")
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
            click.echo(f"remove user: {user_name}")
            if not dry_run:
                response = api1.delete_user(username=user_name)
