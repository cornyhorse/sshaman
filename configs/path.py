import os

# Default config path, located in the .config directory of the users home directory
CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'sshaman')


def get_config_path():
    return CONFIG_PATH


def set_config_path(path):
    global CONFIG_PATH
    CONFIG_PATH = path
