import click

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
@click.option('--type', "-t", required=True, type=click.Choice(['user', 'system']),
              help='The type of group')
@click.pass_context
def create_group(ctx, name, type):
    """
    Create a group
    """
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    response = api2.create_group(name, type)
    logger.info(f"{response}")


@group.command('delete')
@click.option('--name', "-n", required=True, type=str, help='Name of the group')
@click.pass_context
def delete_group(ctx, name):
    """
    Delete a group
    """
    # FIXME: Ideally, this would output JSON info of the deleted group (similar to delete-user), but at the moment it's
    #  unclear exactly how to do that, given the API wrappers that we have.
    api2 = JumpcloudApiV2(ctx.obj.get('key'))
    logger = ctx.obj.get('logger')
    api2.delete_group(name)
    logger.info(f"Group {name} deleted")
