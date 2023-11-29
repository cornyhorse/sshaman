from pprint import pprint
import click
from utils.config import Config

class SSHMan(Config):
    def __init__(self):
        super().__init__()


    def print_group_list(self, group='all'):
        """

        :return:
        """
        for group, servers in self.config.items():
            print(f'Group: {group}')
            for server in servers:
                print(f'  {server["alias"]} - {server["host"]}:{server["port"]}')





    def __str__(self):
        return str(pprint(self.config))


if __name__ == '__main__':
    smn = SSHMan()


    smn.print_group_list()