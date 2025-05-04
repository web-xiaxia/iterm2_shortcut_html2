# -*- coding: utf-8 -*-
import shutil
from datetime import datetime
import json
import os
from typing import Dict, List


class AppConfig:
    py: Dict[str, str]


class VariableTool:
    values: List[str]
    value: str

    def __init__(self, values: List[str]):
        self.values = values
        self.value = values[-1]


class StorageHelper:
    config_home: str = None
    config_path: str = None
    config_bak: bool = False

    def __init__(self, config_home: str, bak: bool = False):
        self.config_home = config_home
        self.config_path = os.path.join(config_home, "config.json")
        self.config_bak = bak

    async def read(self) -> str:
        try:
            with open(self.config_path, 'r') as fp:
                return fp.read()
        except:
            return "{}"

    async def save(self, data: str):
        with open(self.config_path, 'w') as fp:
            fp.write(data)
        if self.config_bak:
            shutil.copy(self.config_path, os.path.join(self.config_home, f"""bak/{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.json"""))

    async def load_py(self) -> Dict[str, str]:
        fp = await self.read()
        return json.load(fp).get("py")

    async def get_custom_trigger(self) -> Dict[str, Dict[str, object]]:
        return {}

    async def get_session_auto_custom_trigger(self) -> List[Dict]:
        return []

    async def get_custom_variable_map(self) -> Dict[str, VariableTool]:
        return {}

    async def get_event_send(self, event_name) -> Dict:
        return None
