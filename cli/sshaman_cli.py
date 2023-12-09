import click
from management.sshman import SSHAMan  # Ensure SSHAMan is importable from your project structure
from entities import Server
from tests.setup_tests import generate_default_config
from tui import tree
from configs import CONFIG_PATH


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        tree.main()


@click.group()
def cli():
    """SSHAMan Command Line Interface."""
    pass


@cli.command()
@click.option('--config_path', required=False, default=None)
def list_all(config_path):
    """List all groups."""
    manager = SSHAMan()
    manager.list_all()


@cli.command()
@click.argument('group_name')
@click.option('--config_path', required=False, default=None)
def make_group(group_name, config_path):
    """Make a group of servers."""
    manager = SSHAMan(config_path=config_path if config_path else CONFIG_PATH)
    manager.make_group(group_name)


@cli.command()
@click.option('--config_path', required=False, default=None)
def initialize_sample(config_path):
    """Initialize sample config."""
    smn = SSHAMan(config_path=config_path if config_path else CONFIG_PATH)
    generate_default_config(smn.config_path)


@cli.command()
@click.argument('group_path')
@click.argument('alias')
@click.argument('host')
@click.argument('user')
@click.option('--port', '-p', required=False, default=22)
@click.option('--identity_file', '-i', required=False, default='')
@click.option('--password', '-P', required=False, default='')
@click.option('--forward_ports', '-fp', required=False, multiple=True)
@click.option('--start_commands', '-sc', required=False, multiple=True)
@click.option('--config_path', required=False)#, default='')
def add_server(group_path, alias, host, user, port=22, config_path=CONFIG_PATH, **kwargs):
    """Add a server to a group."""
    manager = SSHAMan(config_path=config_path if config_path else CONFIG_PATH)
    manager.add_server(group_path, alias, host, user, port, **kwargs)


if __name__ == '__main__':
    cli()
