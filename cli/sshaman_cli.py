import click
from management.sshman import SSHAMan  # Ensure SSHAMan is importable from your project structure
from entities import Server
from tests.setup_tests import generate_default_config
from tui import tree


def create_options_for_model(model_class):
    def decorator(f):
        for field_name, model_field in model_class.__fields__.items():
            default_value = model_field.default
            help_text = f'{field_name} of the server. Default: {default_value}'
            f = click.option(f'--{field_name}', default=default_value, help=help_text)(f)
        return f

    return decorator


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
    manager = SSHAMan(config_path=config_path if config_path else None)
    manager.make_group(group_name)


@cli.command()
@click.option('--config_path', required=False, default=None)
def initialize_sample(config_path):
    """Initialize sample config."""
    smn = SSHAMan()
    generate_default_config(smn.config_path)


@cli.command()
@click.argument('group_path')
@click.argument('alias')
@click.argument('host')
@create_options_for_model(Server)
def add_server(group_path, alias, host, port, user, config_path, **kwargs):
    """Add a server to a group."""
    manager = SSHAMan(config_path=kwargs.pop('config_path', None))
    manager.add_server(group_path, alias, host, **kwargs)


if __name__ == '__main__':
    cli()
