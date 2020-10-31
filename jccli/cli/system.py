import json
import click
from jccli.errors import SystemNotFoundError
from jccli.jc_api_v1 import JumpcloudApiV1


@click.group()
@click.pass_context
def system(ctx):
    """
    Command set for systems
    """
    pass


@system.command("get")
@click.option('--hostname', '-h', required=True, type=str)
@click.pass_context
def get_system(ctx, hostname):
    """
    Detail view of system, outputted in JSON.
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    try:
        response = api1.get_system(hostname=hostname)
        serialized_response = json.dumps(response, indent=2)
        click.echo(f"{serialized_response}")
    except SystemNotFoundError:
        click.echo(f'no system found with hostname {hostname}', err=True)


@system.command('list')
@click.pass_context
def list_systems(ctx, **kwargs):
    """
    List view of systems, outputted in JSON
    """
    filter = {}
    for field_name, value in kwargs.items():
        if value:
            filter[field_name] = value

    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    response = api1.search_systems(filter)
    serialized_response = json.dumps(response, indent=2)
    click.echo(f"{serialized_response}")


@system.command('set')
@click.option('--hostname', required=True, type=str)
@click.option('--allow-multi-factor-authentication/--disallow-multi-factor-authentication', type=bool, default=None)
@click.option('--allow-public-key-authentication/--disallow-public-key-authentication', type=bool, default=None)
@click.option('--allow-ssh-password-authentication/--disallow-ssh-password-authentication', type=bool, default=None)
@click.option('--allow-ssh-root-login/--disallow-ssh-root-login', type=bool, default=None)
@click.option('--display-name', type=str, default=None)
@click.option('--tags', type=str, multiple=True, default=(None,))
@click.pass_context
def set_system(ctx, hostname, **kwargs):
    """
    Set attributes for system `hostname`
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))

    attributes = {key: value for key, value in kwargs.items() if value is not None and value != (None,)}
    print('Attributes are: ' + str(attributes))

    try:
        response = json.dumps(api1.set_system(hostname=hostname, attributes=attributes), indent=2)
        click.echo(f'{response}')
    except SystemNotFoundError:
        click.echo(f'no system found with hostname {hostname}', err=True)


@system.command("delete")
@click.option('--hostname', required=True, type=str)
@click.pass_context
def delete_system(ctx, hostname):
    """
    Delete a system
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    try:
        response = api1.delete_system(hostname=hostname)
        click.echo(f"successfully deleted system {hostname}")
    except SystemNotFoundError:
        click.echo(f'no system found with hostname {hostname}', err=True)
