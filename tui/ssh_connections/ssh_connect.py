import os
import subprocess
import json
import logging


def check_if_ssh_config_exists(config_path):
    """
    Checks if the SSH configuration file exists.

    :param config_path: Path to the JSON configuration file for the SSH connection.
    :return: True if the file exists, False otherwise.
    """
    return True if os.path.exists(config_path) else False


def check_if_ssh_config_is_valid(config_path):
    """
    Checks if the SSH configuration file is valid.

    :param config_path: Path to the JSON configuration file for the SSH connection.
    :return: True if the file is valid, False otherwise.
    """
    try:
        with open(config_path, "r") as json_file:
            config = json.load(json_file)
            if config["user"] and config["host"] and config["port"]:
                return True
            else:
                return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def retrieve_file(config_path):
    """
    Connects to a server via SSH using the configuration specified in the given path.

    :param config_path: Path to the JSON configuration file for the SSH connection.
    """
    if not config_path:
        raise ValueError("Config path is empty.")

    if not check_if_ssh_config_exists(config_path):
        raise FileNotFoundError(f"SSH configuration file not found: {config_path}")

    if not check_if_ssh_config_is_valid(config_path):
        raise ValueError(f"SSH configuration file is invalid: {config_path}")

    with open(config_path, "r") as json_file:
        config = json.load(json_file)
        return config


def connect_shell(config_path):
    config = retrieve_file(config_path)
    command = f"ssh {config['user']}@{config['host']} -p {config['port']}"
    print(f'Running: {command}')
    return command


def connect_sftp(config_path):
    config = retrieve_file(config_path)
    command = f"sftp -P {config['port']} {config['user']}@{config['host']} "
    print(f'Running: {command}')
    return command


if __name__ == '__main__':
    test_path = "/home/matt/.config/test_sshaman"
    value = connect_shell(os.path.join(test_path, "group1", "vm1.json"))
    print(value)
