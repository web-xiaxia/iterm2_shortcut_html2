# -*- coding: utf-8 -*-
import json
import os


class SystemConfig:
    window_height: int
    window_width: int


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

    async def get_config(self) -> SystemConfig:
        val = await self.read()
        json_data = json.loads(val)
        ret = SystemConfig()
        ret.window_width = json_data.get("window_width", 950)
        ret.window_height = json_data.get("window_height", 480)
        return ret
