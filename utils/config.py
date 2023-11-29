import json
import shutil
import os

# Default config path, located in the .config directory of the users home directory
CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'sshaman', 'config.json')

DEFAULT_CONFIG = {
    "group 1": [{
        "alias": "vm1",
        "host": "192.168.1.1",
        "port": 22,
        "identity_file": "~/.ssh/id_rsa",
        "forward_ports": [
            "80:localhost:8080",
            "443:localhost:8443"
        ],
        "start_commands": [
            "echo 'hello world'",
            "ls -la"
        ]

    }],
    "group 2": {}
}


class Config:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.check_config_exists()

    def check_config_exists(self):
        print(self.config_path)
        if not os.path.exists(self.config_path):
            self.create_config()

        self.load_config()

    def create_config(self):
        """Create a new config file at the default path"""
        # Create the parent directory if it doesn't exist
        parent_dir = os.path.dirname(self.config_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # Serialize the dictionary and output to file
        with open(self.config_path, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

    def load_config(self):
        """Load the config file at the default path"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
