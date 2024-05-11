import os
import json

from swiftbots.all_types import IConfiguration


class Configuration(IConfiguration):
    storage: dict[str, any]

    def __init__(self):
        self.storage = {}

    def __getitem__(self, key: str) -> any:
        return self.storage[key]

    def add_dict(self, config: dict[str, any]) -> None:
        self.storage.update(config.copy())

    def add_json_file(self, file_name: str) -> None:
        with open(file_name) as f:
            json_load = json.load(f)
            for i in json_load:

            self.storage.update(json.load(f))

    def add_environment_variables(self, prefix: str = None) -> None:
        pass

    def add_command_line(self, args: list[str]) -> None:
        pass

import sys
c = Configuration()
c.add_dict({"keks": "keks2", "a": 2})
print(c["keks"])
print("a" in c)
