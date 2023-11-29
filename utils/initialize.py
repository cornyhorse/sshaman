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




if __name__ == '__main__':
    home_dir = os.path.expanduser('~')
    test_config_path = os.path.join(home_dir, '.config', 'test_sshaman')
    print(test_config_path)
    smn = SSHAMan(config_path=test_config_path)
    smn.list_all()
