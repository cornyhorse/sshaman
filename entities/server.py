import json
import os
from pydantic import BaseModel, Field, field_validator, ConfigDict


class Server(BaseModel):
    alias: str
    host: str
    port: int = Field(default=22, ge=0, le=65535)
    user: str = None
    identity_file: str = None
    password: str = None
    forward_ports: list[str] = None
    start_commands: list[str] = None
    server_group_path: str = None

    model_config = {
        'extra': 'forbid',
        'validate_assignment': True
    }

    def __str__(self):
        print(f'  {self.alias} - {self.host}:{self.port}')

    @field_validator('port')
    def validate_port(cls, value):
        if not 0 <= value <= 65535:
            raise ValueError("Port must be between 0 and 65535")
        return value

    @field_validator('user')
    def validate_user(cls, v):
        if not v:
            raise ValueError("User must not be empty")
        return v

    def save_config(self, server_group_path):
        """Save the config file in the server group directory"""

        self.server_group_path = server_group_path
        config = self.serialize()

        absolute_path = os.path.join(self.server_group_path, f'{self.alias}.json')
        absolute_path = os.path.normpath(absolute_path)
        print(f'Saving config to {absolute_path}')
        with open(absolute_path, 'w') as f:
            json.dump(config, f, indent=4)

    def serialize(self):
        return json.loads(self.model_dump_json(indent=4))

