from pprint import pprint
import click
from utils.initialize import SSHAMan
from tests.generate_test_configurations import generate_default_config


class SSHMan(SSHAMan):
    def __init__(self):
        super().__init__()

    def print_group_list(self, group_filter='all'):
        for group, servers in self.config.items():
            print(group)
            print(type(group))
            print(servers)
            print(type(servers))
            # if group_filter == 'all' or group == group_filter:
                # print(f'Group: {group}')
                # for server in servers:
                #     print(f'  {server["alias"]} - {server["host"]}:{server["port"]}')

    def add_group(self, group_name):
        self.config[group_name] = []
        self.save_config()

    def __str__(self):
        return str(pprint(self.config))

@click.command()
@click.option('--group-filter', default=None, help='List groups of servers')
@click.option('--add-group', default=None, help='Add a group of servers')
def main(group_filter, add_group):
    smn = SSHMan()

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