# -*- coding: utf-8 -*-
import shutil
from datetime import datetime, timedelta
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
            await self.delete_files_older_than_15_days(os.path.join(self.config_home, "bak"))

    async def delete_files_older_than_15_days(self, dir_path: str):
        # 获取当前时间
        now = datetime.now()
        # 计算15天前的日期
        threshold_date = now - timedelta(days=15)

        # 遍历目录下的所有文件和目录
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 获取文件的修改时间
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                # 如果文件修改时间早于15天前的日期，则删除文件
                if file_mtime < threshold_date:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")

    async def load_py(self) -> Dict[str, str]:
        fp = await self.read()
        return json.loads(fp).get("py")

    async def get_custom_trigger(self) -> Dict[str, Dict[str, object]]:
        return {}

    async def get_session_auto_custom_trigger(self) -> List[Dict]:
        return []

    async def get_custom_variable_map(self) -> Dict[str, VariableTool]:
        return {}

    async def get_event_send(self, event_name) -> Dict:
        return None
