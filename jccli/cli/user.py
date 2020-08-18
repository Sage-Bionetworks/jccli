import json
import click

from jccli.jc_api_v1 import JumpcloudApiV1


@click.group()
@click.pass_context
def user(ctx):
    """
    Command set for users
    """
    pass


@user.command('create')
@click.option('--username', '-u', required=True, type=str)
@click.option('--email', '-e', required=True, type=str)
@click.option('--firstname', '-f', type=str, default='')
@click.option('--lastname', '-l', type=str, default='')
@click.option('--allow-public-key/--disallow-public-key', default=True)
@click.option('--ldap-binding-user', is_flag=True)
@click.option('--passwordless-sudo', is_flag=True)
@click.option('--sudo', is_flag=True)
@click.pass_context
def create_user(ctx, username, email, firstname, lastname, allow_public_key, ldap_binding_user, passwordless_sudo,
                sudo):
    """
    Create a new user
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    systemuser = {
        'username': username,
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'allow_public_key': str(allow_public_key),
        'ldap_binding_user': str(ldap_binding_user),
        'passwordless_sudo': str(passwordless_sudo),
        'sudo': str(sudo)
    }
    response = json.dumps(api1.create_user(systemuser), indent=2)
    logger.info(f"{response}")


@user.command("get")
@click.option('--username', '-u', required=True, type=str)
@click.pass_context
def get_user(ctx, username):
    """
    Detail view of user, outputted in JSON.
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    response = api1.get_user(username=username)
    serialized_response = json.dumps(response, indent=2)
    logger.info(f"{serialized_response}")


@user.command('list')
@click.option('--firstname', '-f', default=None, type=str)
@click.option('--lastname', '-l', default=None, type=str)
@click.pass_context
def list_users(ctx, **kwargs):
    """
    List view of users, outputted in JSON
    """
    filter = {}
    for field_name, value in kwargs.items():
        if value:
            filter[field_name] = value

    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    response = api1.search_users(filter)
    serialized_response = json.dumps(response, indent=2)
    logger.info(f"{serialized_response}")


@user.command('set')
@click.option('--username', '-u', required=True, type=str)
@click.option('--email', '-e', default=None, type=str)
@click.option('--firstname', '-f', default=None, type=str)
@click.option('--lastname', '-l', default=None, type=str)
@click.pass_context
def set_user(ctx, username, email, firstname, lastname):
    api1 = JumpcloudApiV1(ctx.obj.get('key'))

    attributes = {}
    if email is not None:
        attributes['email'] = email
    if firstname is not None:
        attributes['firstname'] = firstname
    if lastname is not None:
        attributes['lastname'] = lastname

    response = json.dumps(api1.set_user(username, attributes=attributes), indent=2)
    logger = ctx.obj.get('logger')
    logger.info(f'{response}')


@user.command("delete")
@click.option('--username', "-u", required=True, type=str)
@click.pass_context
def delete_user(ctx, username):
    """
    Delete a user
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    response = api1.delete_user(username=username)
