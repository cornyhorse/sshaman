import os

from configs import set_config_path
from management.sshman import SSHAMan


def dev_list_all():
    home_dir = os.path.expanduser('~')
    test_config_path = os.path.join(home_dir, '.config', 'test_sshaman')
    set_config_path(test_config_path)

    # Removing test config path to test initialization
    import shutil
    if os.path.exists(os.path.normpath(test_config_path)):
        shutil.rmtree(os.path.normpath(test_config_path))

    # Generating default config
    from tests.setup_tests import generate_default_config
    generate_default_config(test_config_path)

    smn = SSHAMan(config_path=test_config_path)
    smn.make_group('group1.subgroup1.subgroup2')

    _dev_list_all()


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


def dev_make_group():
    home_dir = os.path.expanduser('~')
    test_config_path = os.path.join(home_dir, '.config', 'test_sshaman')
    smn = SSHAMan(config_path=test_config_path)
    # smn.make_group('group1')
    # smn.make_group(group_path='group1.sg1')
    smn.make_group('group1.subgroup1.subgroup2')


def _dev_list_all():
    home_dir = os.path.expanduser('~')
    test_config_path = os.path.join(home_dir, '.config', 'test_sshaman')
    smn = SSHAMan(config_path=test_config_path)
    smn.list_all()

if __name__ == '__main__':
    dev_list_all()
    # dev_add_server()
    # dev_make_group()
    # _dev_list_all()