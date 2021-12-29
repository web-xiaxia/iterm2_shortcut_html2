# -*- coding: utf-8 -*-
from common.utils import singleton
from typing import Dict
import json
import os


@singleton
class SystemStorageData:

    def __init__(self, main_home):
        self.storage = None
        self.storage_path = os.path.join(main_home, 'system.json')
        self.main_home = main_home

    async def get_storage(self) -> Dict:
        if self.storage is not None:
            return self.storage

        print(f"system storage 打开了文件")
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as fp:
                fp.write(json.dumps({
                    'storage_path': self.main_home,
                    'storage_history_path': os.path.join(self.main_home, 'storage_history')
                }))
        with open(self.storage_path, 'r') as fp:
            self.storage = json.load(fp)

        return self.storage

    async def set_storage_path(self, storage_path: str, storage_history_path: str):
        storage = await self.get_storage()
        if storage_path and os.path.isdir(storage_path):
            storage['storage_path'] = storage_path
        if storage_history_path and os.path.isdir(storage_history_path):
            storage['storage_history_path'] = storage_history_path
        with open(self.storage_path, 'w') as fp:
            fp.write(json.dumps(self.storage, sort_keys=True, indent=4))
