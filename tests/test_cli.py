import os
import pytest
from click.testing import CliRunner
from cli.sshaman_cli import cli

from tests.setup_tests import sshaman_setup


@pytest.fixture
def runner():
    return CliRunner()


def test_list_all(sshaman_setup, runner, capsys):
    smn, test_config_path = sshaman_setup

    # Invoke the CLI command
    result = runner.invoke(cli, ['list-all', '--config_path', test_config_path])
    print(result.output)  # Add this line to print the output
    # Check if the command was successful
    assert result.exit_code == 0

    # Capture the printed output
    captured = capsys.readouterr()
    output = captured.out

    # Define the expected output
    expected_output = """├── group1/
│   ├── vm2 - 192.168.1.100:22
│   ├── vm1 - 192.168.1.100:22
│   ├── subgroup1/
│   │   ├── subgroup2/
├── group2/
"""

    expected_output = expected_output.strip().replace('    ', '\t')
    output = output.strip().replace('    ', '\t')
    assert output.strip() == expected_output.strip()

# # Test for make-group command
# def test_make_group(sshaman_setup, runner, capsys):
#     group_name = 'group3'
#     result = runner.invoke(cli, ['make-group', group_name])
#     print(result.output)
#
#     expected_output = f'Group created at {group_name}'
#     expected_output = expected_output.strip().replace('    ', '\t')
#     output = result.output.strip().replace('    ', '\t')
#     assert output.strip() == expected_output.strip()
#
#     assert 'Group created' in result.output  # Replace with expected success message
#
# # Test for add-server command
# def test_add_server(runner):
#     group_path = 'test_group'
#     alias = 'test_alias'
#     host = 'test_host'
#     result = runner.invoke(cli, ['add-server', group_path, alias, host, '--port', '22'])
#     assert result.exit_code == 0
#     assert 'Server added' in result.output  # Replace with expected success message

