import json
import click
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
    except SystemNotFoundError:
        pass
    serialized_response = json.dumps(response, indent=2)
    click.echo(f"{serialized_response}")


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
