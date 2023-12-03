import os
import json
from pydantic import BaseModel, Field, root_validator, field_validator, ConfigDict
from typing import Optional, List, Dict

from configs import CONFIG_PATH, get_config_path


class ServerGroup(BaseModel):
    group_name: str
    children: Dict[str, 'ServerGroup'] = {}  # Store children in a dictionary
    sshaman_path: str = get_config_path()

    # The relative path is the parent of sshaman path if otherwise not provided.
    relative_path: str = ''

    @property
    def absolute_path(self):
        if self.relative_path:
            local_dir = os.path.join(self.sshaman_path, self.relative_path)
        else:
            local_dir = os.path.join(self.sshaman_path, self.group_name)
        return os.path.normpath(local_dir)

    def __init__(self, **data):
        super().__init__(**data)
        self.sshaman_path = os.path.normpath(self.sshaman_path)
        print(f"Initializing ServerGroup: {self.group_name}")
        self._initialize()

    def _initialize(self):
        """
        Creates a directory for the group.
        :return:
        """

        if not os.path.exists(self.absolute_path):
            print(f'Creating directory {self.absolute_path}')
            os.makedirs(self.absolute_path)
        else:
            print(f'Directory {self.absolute_path} already exists.')

    def make_child(self, group_name, parent_absolute_path):
        """
        Create a child group.

        :param group_name:
        :param parent_absolute_path:
        :return:
        """
        child_group = ServerGroup(group_name=group_name, relative_path=parent_absolute_path,
                                  sshaman_path=self.sshaman_path)
        child_group._initialize()  # Initialize the child group
        self.children[group_name] = child_group

    def add_server(self, server):
        server.save_config(server_group_path=self.absolute_path)

    def __str__(self):
        return self.group_name

    def __getattr__(self, item):
        """Allow attribute-style access to children."""
        if item in self.children:
            return self.children[item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    model_config = {
        'extra': 'forbid',
        'validate_assignment': True
    }
