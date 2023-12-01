import json
import os
import shutil
import pytest
from configs import set_config_path
from tests.generate_test_configurations import generate_default_config
from utils.initialize import SSHAMan

@pytest.fixture(scope="module")
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

    yield smn, test_config_path

    # Teardown
    if os.path.exists(os.path.normpath(test_config_path)):
        shutil.rmtree(os.path.normpath(test_config_path))

def test_load_config(sshaman_setup):
    """
    Test that the config is loaded correctly.

    The test configuration contains these paths/files:
    ~/.config/test_sshaman/
    ~/.config/test_sshaman/group1/
    ~/.config/test_sshaman/group1/sg1/
    ~/.config/test_sshaman/group1/sg1/vm2.json
    ~/.config/test_sshaman/group1/vm1.json
    ~/.config/test_sshaman/group2/

    This test checks to see that this structure is identical to the above and that vm1 and vm2 contain the correct
    contents and ONLY the correct contents.
    """
    smn, test_config_path = sshaman_setup

    group1 = os.path.join(test_config_path, 'group1')
    vm1 = os.path.join(group1, 'vm1.json')

    assert os.path.exists(vm1)

    with open(vm1, 'r') as f:
        vm1_json = json.load(f)
        correct_contents = {
            "alias": "vm1",
            "host": "192.168.1.100",
            "port": 22,
            "user": "root",
            "identity_file": "~/.ssh/id_rsa",
            "password": "12345",
            "forward_ports": [
                "80:localhost:8080",
                "443:localhost:8443"
            ],
            "start_commands": [
                "echo 'hello world'",
                "ls -la"
            ],
            "server_group_path": os.path.join(test_config_path, "group1")
        }
        assert vm1_json == correct_contents

    # Assert that group1 contains sg1 and vm1
    path_content = os.listdir(group1)
    correct_contents = ['sg1', 'vm1.json']
    assert sorted(path_content) == sorted(correct_contents)

    # Assert that sg1 contains vm2
    subgroup1 = os.path.join(group1, 'sg1')
    vm2 = os.path.join(subgroup1, 'vm2.json')
    with open(vm2, 'r') as f:
        vm2_json = json.load(f)
        correct_contents = {
            "alias": "vm2",
            "host": "192.168.1.100",
            "port": 22,
            "user": "root",
            "identity_file": "~/.ssh/id_rsa",
            "password": "12345",
            "forward_ports": [
                "80:localhost:8080",
                "443:localhost:8443"
            ],
            "start_commands": [
                "echo 'hello world'",
                "ls -la"
            ],
            "server_group_path": os.path.join(test_config_path, "group1", "sg1")
        }
        assert vm2_json == correct_contents

    # Assert that sg1 ONLY contains vm2
    path_content = os.listdir(subgroup1)
    correct_contents = ['vm2.json']
    assert sorted(path_content) == sorted(correct_contents)

    # Check existence of group2 and its emptiness
    group2 = os.path.join(test_config_path, 'group2')
    assert os.path.exists(group2)
    path_content = os.listdir(group2)
    correct_contents = []
    assert path_content == correct_contents

def test_list_all(sshaman_setup, capsys):
    """
    Test that the list_all method returns the correct output.
    """
    smn, _ = sshaman_setup
    smn.list_all()

    # Capture the printed output
    captured = capsys.readouterr()
    output = captured.out

    correct_output = """
group1:
    vm1 - 192.168.1.100:22
    sg1:
        vm2 - 192.168.1.100:22

group2:
        No servers in configuration path."""

    # Normalize newlines and spaces for cross-platform compatibility and consistent formatting
    correct_output = correct_output.strip().replace('    ', '\t')
    output = output.strip().replace('    ', '\t')

    assert output == correct_output
