import os
import shutil

import pytest

from configs import set_config_path
from management.sshman import SSHAMan
from tests.generate_test_configurations import generate_default_config


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
