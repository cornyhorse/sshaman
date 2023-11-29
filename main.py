from pprint import pprint
import click
from utils.config import Config


class SSHMan(Config):
    def __init__(self):
        super().__init__()

    def print_group_list(self, group_filter='all'):
        """

        :return:
        """
        for group, servers in self.config.items():
            if group == 'all' or group == group_filter:
                print(f'Group: {group}')
                for server in servers:
                    print(f'  {server["alias"]} - {server["host"]}:{server["port"]}')

    def __str__(self):
        return str(pprint(self.config))


@click.command()
@click.option('--group_filter', default='all', help='List groups of servers')
def print_group_list(group_filter):
    smn = SSHMan()
    groups = smn.get_group_list(group_filter)
    for group, servers in groups.items():
        print(f'Group: {group}')
        for alias, host, port in servers:
            print(f'  {alias} - {host}:{port}')


if __name__ == '__main__':
    smn = SSHMan()

    smn.print_group_list()
