import json
import os


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
        if config.get('user') is None:
            config['user'] = get_user_from_os()

        if config.get('password'):
            raise NotImplementedError("Password authentication is not supported yet.")

        if config.get('identity_file'):
            config['identity_file'] = find_identity_file(config['identity_file'])
        else:
            # Declare the default identity file of id_rsa
            config['identity_file'] = os.path.join(get_user_ssh_dir_from_home(), 'id_rsa')

        return config


def get_user_from_os():
    """
    Attempt to get the user from the OS; assumes that the user you are trying to connect is the same as the user
    that is invoking the command.
    :return:
    """
    return os.getlogin()


def get_user_ssh_dir_from_home():
    """
    Gets the SSH directory for the current user.
    :return:
    """
    return os.path.join(os.path.expanduser('~'), '.ssh')


def find_identity_file(identity_file):
    """
    Finds the identity file from the SSH directory.
    :param identity_file:
    :return:
    """
    # Determine if the identity file is just the name of a file or if it's a path:
    if os.path.isabs(identity_file) or identity_file.startswith('~'):
        if os.path.exists(identity_file):
            return identity_file
        else:
            raise FileNotFoundError(f"Identity file not found: {identity_file}")
    else:
        ssh_dir = get_user_ssh_dir_from_home()
        identity_file_path = os.path.join(ssh_dir, identity_file)
        if os.path.exists(identity_file_path):
            return identity_file_path
        else:
            raise FileNotFoundError(f"Identity file not found: {identity_file_path}")


def remove_double_spaces(string):
    """
    Removes double spaces from a string.
    :param string:
    :return:
    """
    return ' '.join(string.split())


def connect_shell(config_path):
    config = retrieve_file(config_path)

    # fp = ''
    # if config.get('forward_ports'):
    #     for p in config['forward_ports']:
    #         fp += f' -L {p} '

    idf = f'-i {config["identity_file"]}'

    # command = f"ssh {fp} {idf} {config['user']}@{config['host']} -p {config['port']}"
    command = f"ssh {idf} {config['user']}@{config['host']} -p {config['port']}"
    command = remove_double_spaces(command)

    # if config.get('start_commands'):
    #     raise NotImplementedError("Start commands are not supported yet.")
    #     command = [command] + config['start_commands']

    return command


def connect_sftp(config_path):
    config = retrieve_file(config_path)

    idf = f"-i {config['identity_file']} "

    command = f"sftp {idf} -P {config['port']} {config['user']}@{config['host']} "
    command = remove_double_spaces(command)
    return command


if __name__ == '__main__':
    test_path = "/home/matt/.config/test_sshaman"
    value = connect_shell(os.path.join(test_path, "group1", "vm1.json"))
    print(value)
