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
        """List all groups and server details in a tree-like structure."""
        for root, dirs, files in os.walk(self.config_path):
            if root == self.config_path:
                # Skip the root directory
                continue

            level = root.replace(self.config_path, '').count(os.sep)
            indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
            print(f'{indent}{os.path.basename(root)}/')

            subindent = '│   ' * level
            for fname in files:
                if fname.endswith('.json'):
                    file_path = os.path.join(root, fname)
                    with open(file_path, 'r') as f:
                        config = json.load(f)
                        alias = config.get('alias', '')
                        host = config.get('host', '')
                        port = config.get('port', '')
                        print(f'{subindent}├── {alias} - {host}:{port}')

    def make_group(self, group_name):
        groups = group_name.split('.')
        parent_group = None
        current_path = ""

        for group in groups:
            if parent_group is None:
                # For the first group, just set it directly
                parent_group = ServerGroup(group_name=group, sshaman_path=self.config_path)
                current_path = group  # Set the initial current path
            else:
                current_path = os.path.join(current_path, group)  # Update the path
                subgroup = ServerGroup(group_name=group, sshaman_path=self.config_path, relative_path=current_path)
                parent_group.make_child(subgroup.group_name, parent_group.absolute_path)  # Pass the absolute path
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
