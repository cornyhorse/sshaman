from pprint import pprint
import json
import os

from configs import get_config_path, set_config_path



class SSHAMan:
    def __init__(self, config_path=get_config_path()):
        # If a custom config path is provided, overwrite the global variable with the custom path.
        if config_path != get_config_path():
            set_config_path(config_path)
        self.config_path = config_path

        self.check_config_exists()
        self.config = []

    def check_config_exists(self):
        if not os.path.exists(self.config_path):
            # Create the parent directory if it doesn't exist
            parent_dir = os.path.dirname(self.config_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            payload = {'Information': 'This is the default config file for SSHaman. Please do not remove this file!',
                       'About': 'Each directory in this directory represents a group of servers. Each directory may '
                                'contain an arbitrary number of servers. Each server is represented by a JSON file.'}
            with open(self.config_path, 'w') as f:
                json.dump(payload, f, indent=4)
        # else:
        #     self.load_config()

    def create_default_config(self):
        """Create a new config file at the default path"""
        # Create the parent directory if it doesn't exist
        parent_dir = os.path.dirname(self.config_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        group_list = default_config()
        self.serialize(group_list)
        self.save_config()

    # def load_config(self):
    #     """Load the config file at the default path"""
    #     with open(self.config_path, 'r') as f:
    #         self.config = json.load(f)

    def save_config(self):
        """Save the config file at the default path"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def serialize(self, group_list):
        serialized_list = serialize_server_group_list(group_list)
        self.config = serialized_list
        print(type(serialized_list))
        pprint(serialized_list)
        # self.config = json.dumps(serialized_list, indent=4)



