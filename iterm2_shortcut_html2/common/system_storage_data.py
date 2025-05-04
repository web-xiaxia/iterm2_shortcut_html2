# -*- coding: utf-8 -*-
import os


class SystemStorageHelper:
    config_home: str = None
    config_path: str = None

    def __init__(self, config_home: str):
        self.config_home = config_home
        self.config_path = os.path.join(config_home, "system_config.json")

    async def read(self) -> str:
        try:
            with open(self.config_path, 'r') as fp:
                return fp.read()
        except:
            return "{}"

    async def save(self, data: str):
        with open(self.config_path, 'w') as fp:
            fp.write(data)
