import os
import shutil

import pytest

from configs import set_config_path
from management.sshman import SSHAMan


@pytest.fixture(scope="function")
def sshaman_setup():
    home_dir = os.path.expanduser('~')
    test_config_path = os.path.join(home_dir, '.config', 'test_sshaman')
    set_config_path(test_config_path)

    # Removing test config path to test initialization
    if os.path.exists(os.path.normpath(test_config_path)):
        shutil.rmtree(os.path.normpath(test_config_path))

    # Generating default config
    generate_default_config(test_config_path)

    smn = SSHAMan(config_path=test_config_path)
    smn.make_group('group1.subgroup1.subgroup2')
    yield smn, test_config_path

    # Teardown
    # if os.path.exists(os.path.normpath(test_config_path)):
    #     shutil.rmtree(os.path.normpath(test_config_path))


def generate_default_config(test_config_path):
    from entities import ServerGroup, Server
    print("Generating default config...")
    g1 = ServerGroup(group_name='group1', sshaman_path=test_config_path)
    g1.make_child('sg1', parent_absolute_path=g1.absolute_path)
    s = Server(
        alias='vm1',
        host='192.168.1.100',
        port=22,
        user='root',
        password='12345',
        identity_file='~/.ssh/id_rsa',
        forward_ports=[
            '80:localhost:8080',
            '443:localhost:8443'
        ],
        start_commands=["echo 'hello world'", "ls -la"]
    )
    g1.add_server(s)


    s2 = Server(
        alias='vm2',
        host='192.168.1.100',
        port=22,
        user='root',
        password='12345',
        identity_file='~/.ssh/id_rsa',
        forward_ports=[
            '80:localhost:8080',
            '443:localhost:8443'
        ],
        start_commands=["echo 'hello world'", "ls -la"]
    )

    sg2 = g1.children['sg1']
    sg2.add_server(s2)
    g2 = ServerGroup(group_name='group2', sshaman_path=test_config_path)
    group_list = [g1, g2]
    return group_list

if __name__ == '__main__':
    generate_default_config('/home/matt/.config/test_sshaman')