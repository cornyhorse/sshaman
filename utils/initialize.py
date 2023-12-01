from pprint import pprint
import json
import os

from configs import get_config_path, set_config_path
from entities import Server, ServerGroup


class SSHAMan:
    def __init__(self, config_path=get_config_path()):
        # If a custom config path is provided, overwrite the global variable with the custom path.
        if config_path != get_config_path():
            set_config_path(config_path)
        self.config_path = config_path

    def list_all(self):
        """List all groups"""
        for root, dirs, files in os.walk(self.config_path):
            if root != self.config_path:
                relative_path = root.replace(self.config_path, '')
                split_path = relative_path.split('/')
                split_path = [x for x in split_path if x != '']
                depth = len(split_path) - 1
                group_name = os.path.basename(root)
                indent = '\t' * depth
                print(f'{indent}{group_name}:')
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            config = json.load(f)
                            indent = '\t' * (depth + 1)
                            print(f'{indent}{config["alias"]} - {config["host"]}:{config["port"]}')
                if len(files) == 0:
                    print('\t\tNo servers in configuration path.')

                if len(dirs) == 0 and depth != 0:
                    print('')

    def make_group(self, group_name):
        """
        Make a group of servers.
        :param group_name: Name of the group to make. Can be a list of servers separated by '.' notation, e.g.
                           'group1.subgroup1.subgroup2'

        """
        groups = group_name.split('.')
        for i, group in enumerate(groups):
            if i == 0:
                parent_group = ServerGroup(group_name=group, sshaman_path=self.config_path)
            else:
                subgroup = ServerGroup(group_name=group, sshaman_path=self.config_path, relative_path=groups[i - 1])
                parent_group.make_child(subgroup.group_name)
                parent_group = subgroup

        return parent_group

    def add_server(self, group_path, alias, host, **kwargs):
        """
        Add a server to a group.
        :param alias:
        :param host:
        :param kwargs:
        :return:
        """
        last_group = self.make_group(group_path)

        # Create a server and add it to the last group
        server_data = {'alias': alias, 'host': host, **kwargs}
        server = Server(**server_data)
        last_group.add_server(server)


def dev_list_all():
    home_dir = os.path.expanduser('~')
    test_config_path = os.path.join(home_dir, '.config', 'test_sshaman')
    smn = SSHAMan(config_path=test_config_path)
    smn.list_all()


def dev_make_group():
    home_dir = os.path.expanduser('~')
    test_config_path = os.path.join(home_dir, '.config', 'test_sshaman')
    smn = SSHAMan(config_path=test_config_path)
    # smn.make_group('group1')
    smn.make_group(group_path='group1.sg1')


def dev_add_server():
    home_dir = os.path.expanduser('~')
    test_config_path = os.path.join(home_dir, '.config', 'test_sshaman')
    smn = SSHAMan(config_path=test_config_path)

    smn.add_server(
        group_path='group1.sg1',
        alias='vm3',
        host='192.168.1.100',
        port=22,
        user='root',
        identity_file='~/.ssh/id_rsa',
        password='12345',
        forward_ports=['80:localhost:8080', '443:localhost:8443'],
        start_commands=["echo 'hello world'", "ls -la"],
        server_group_path='/home/matt/.config/test_sshaman/group1/sg1'
    )


if __name__ == '__main__':
    # dev_list_all()
    # dev_make_group()
    dev_add_server()
