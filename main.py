from pprint import pprint
import click
from utils.initialize import SSHAMan
from tests.generate_test_configurations import generate_default_config


@click.command()
@click.option('--group-filter', default=None, help='List groups of servers')
@click.option('--add-group', default=None, help='Add a group of servers')
def main(group_filter, add_group):
    smn = SSHAMan()

    if add_group:
        smn.add_group(add_group)
        print(f"Group '{add_group}' added.")

    if group_filter:
        smn.print_group_list(group_filter)
    elif add_group is None:
        # If no filter is provided and no group was added, show all groups
        smn.print_group_list('all')


def dev():
    generate_default_config()


if __name__ == '__main__':
    # main()
    dev()
