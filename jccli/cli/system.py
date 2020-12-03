import json
import click
from jccli.jc_api_v1 import JumpcloudApiV1


@click.group()
@click.pass_context
def system(ctx):
    """
    Command set for systems.
    """
    pass


@system.command("get")
@click.option('--id', '-i', 'system_id', required=True, type=str, help="The system ID")
@click.pass_context
def get_system(ctx, system_id):
    """
    Detail view of system.
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    response = api1.get_system(system_id=system_id)
    serialized_response = json.dumps(response, indent=2)
    click.echo(f"{serialized_response}")


@system.command('list')
@click.option('--active/--inactive', type=bool, default=None)
@click.option('--arch', type=str, default=None, help='architecture')
@click.option('--display-name', 'displayName', type=str, default=None)
@click.option('--hostname', type=str, default=None)
@click.option('--os', type=str, default=None)
@click.option('--remote-ip', 'remoteIp', default=None)
@click.pass_context
def list_systems(ctx, **kwargs):
    """
    List view of systems. Show systems which match the selected options. Return all systems if no options are selected.
    """
    filter = {}
    for field_name, value in kwargs.items():
        if value is not None:
            filter[field_name] = value

    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    response = api1.search_systems(filter)
    serialized_response = json.dumps(response, indent=2)
    click.echo(f"{serialized_response}")


@system.command('set')
@click.option('--id', '-i', 'system_id', required=True, type=str, help='The system ID')
@click.option('--allow-multi-factor-authentication/--disallow-multi-factor-authentication', type=bool, default=None)
@click.option('--allow-public-key-authentication/--disallow-public-key-authentication', type=bool, default=None)
@click.option('--allow-ssh-password-authentication/--disallow-ssh-password-authentication', type=bool, default=None)
@click.option('--allow-ssh-root-login/--disallow-ssh-root-login', type=bool, default=None)
@click.option('--display-name', type=str, default=None)
@click.pass_context
def set_system(ctx, system_id, **kwargs):
    """
    Set attributes for system with given ID.
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))

    attributes = {key: value for key, value in kwargs.items() if value is not None and value != (None,)}

    response = json.dumps(api1.set_system(system_id=system_id, attributes=attributes), indent=2)
    click.echo(f'{response}')


@system.command("delete")
@click.option('--id', '-i', 'system_id', required=True, type=str, help='The system ID')
@click.pass_context
def delete_system(ctx, system_id):
    """
    Delete a system.
    """
    api1 = JumpcloudApiV1(ctx.obj.get('key'))
    response = api1.delete_system(system_id=system_id)
    click.echo(f"successfully deleted system {system_id}")
