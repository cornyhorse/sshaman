import click
from management.sshman import SSHAMan  # Ensure SSHAMan is importable from your project structure


@click.group()
def cli():
    """SSHAMan Command Line Interface."""
    pass


@cli.command()
@click.option('--config_path', required=False, default=None)
def list_all(config_path):
    """List all groups."""
    manager = SSHAMan(config_path=config_path if config_path else None)
    manager.list_all()


@cli.command()
@click.argument('group_name')
@click.option('--config_path', required=False, default=None)
def make_group(group_name, config_path):
    """Make a group of servers."""
    manager = SSHAMan(config_path=config_path if config_path else None)
    manager.make_group(group_name)


@cli.command()
@click.argument('group_path')
@click.argument('alias')
@click.argument('host')
@click.option('--port', default=22, help='Port number.')
@click.option('--user', default=None, help='Username for SSH.')
@click.option('--config_path', required=False, default=None)
def add_server(group_path, alias, host, port, user, config_path):
    """Add a server to a group."""
    manager = SSHAMan(config_path=config_path if config_path else None)
    kwargs = {'port': port, 'user': user} if user else {'port': port}
    manager.add_server(group_path, alias, host, **kwargs)


if __name__ == '__main__':
    cli()
