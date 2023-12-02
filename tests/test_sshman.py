import json
import os

from entities.server import Server
from entities.server_group import ServerGroup

from tests.setup_tests import sshaman_setup
from tests.util_tests import print_diff


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
    correct_contents = ['subgroup1', 'vm1.json', 'vm2.json']

    actual = sorted(path_content)
    expected = sorted(correct_contents)
    if actual != expected:
        print_diff(expected=expected, actual=actual)


    assert sorted(path_content) == sorted(correct_contents)

    # Assert that sg1 contains vm2
    subgroup1 = os.path.join(group1, 'subgroup1')
    vm2 = os.path.join(group1, 'vm2.json')
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
            "server_group_path": os.path.join(test_config_path, "group1")
        }
        assert vm2_json == correct_contents

    # Assert that sg1 ONLY contains vm2
    path_content = os.listdir(subgroup1)
    correct_contents = ['subgroup2']
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

    correct_output = """├── group1/
│   ├── vm2 - 192.168.1.100:22
│   ├── vm1 - 192.168.1.100:22
│   ├── subgroup1/
│   │   ├── subgroup2/
├── group2/
"""

    # Normalize newlines and spaces for cross-platform compatibility and consistent formatting
    print("-"*50)
    print("Actual Output vs. Expected Output:")
    print_diff(expected=correct_output, actual=output)
    print("-" * 50)
    correct_output = correct_output.strip().replace('    ', '\t')
    output = output.strip().replace('    ', '\t')

    assert output == correct_output

def test_make_group_single(sshaman_setup):
    smn, _ = sshaman_setup
    group_name = "group1"
    created_group = smn.make_group(group_name)
    assert isinstance(created_group, ServerGroup)
    assert os.path.exists(os.path.join(smn.config_path, group_name))

def test_make_group_nested(sshaman_setup):
    smn, _ = sshaman_setup
    group_name = "group1.subgroup1.subgroup2"
    created_group = smn.make_group(group_name)

    # Assert that the final group in the hierarchy is returned
    assert isinstance(created_group, ServerGroup)
    assert created_group.group_name == 'subgroup2'

    # Check if each nested group's directory is created
    group1_path = os.path.join(smn.config_path, 'group1')
    subgroup1_path = os.path.join(group1_path, 'subgroup1')
    subgroup2_path = os.path.join(subgroup1_path, 'subgroup2')

    assert os.path.exists(group1_path)
    assert os.path.exists(subgroup1_path)
    assert os.path.exists(subgroup2_path)
    #
    # Optionally, assert parent-child relationships if such properties are accessible
    # ...

