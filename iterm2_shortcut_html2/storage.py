# -*- coding: utf-8 -*-
import time

from datetime import datetime

from os.path import abspath, dirname
import shutil
from functools import wraps
from typing import Dict, Tuple
import json
import os

INIT_CONFIG_JSON = {
    "tabs": [{
        "name": "tab1",
        "tab_id": "1",
        "tab_groups": [
            {
                "buttons": [
                    {
                        "type": "send_text",
                        "name": "button1",
                        "send_text": "1243243243223"
                    }
                ]
            }
        ]
    }]
}


def singleton(f):
    instance = {}

    @wraps(f)
    def getinstance(*args, **kwargs):
        if f not in instance:
            instance[f] = f(*args, **kwargs)
        return instance[f]

    return getinstance


@singleton
class Storage:

    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.storage = None
        self.storage_history_home = os.path.join(abspath(dirname(__file__)), './storage_history')
        self.temp_storage = {}
        self.last_bak_time = 0
        self.last_bak_path = None

    async def reset_xpy_method(self):
        if 'py_method' in self.temp_storage:
            del self.temp_storage['py_method']

    async def get_xpy_method(self):
        if 'py_method' in self.temp_storage:
            return self.temp_storage['py_method']
        storage = await self.get_storage()
        custom_variable_map = await self.reset_custom_variable_map()
        py_method = XPyMethod(storage.get('py_method', []) or [], custom_variable_map)
        self.temp_storage['py_method'] = py_method
        return py_method

    async def reset_event_send_map(self):
        if 'event_send_map' in self.temp_storage:
            del self.temp_storage['event_send_map']

    async def get_event_send_map(self) -> Dict:
        if 'event_send_map' in self.temp_storage:
            return self.temp_storage['event_send_map']
        event_send_map = {}
        storage = await self.get_storage()
        for event_send in storage.get('event_send_text', []):
            if event_send.get("name"):
                event_send_map[event_send.get("name")] = event_send
        self.temp_storage['event_send_map'] = event_send_map
        return event_send_map

    async def get_event_send(self, event_name: str) -> Dict:
        event_send_map = await self.get_event_send_map()
        return event_send_map.get(event_name)

    async def reset_custom_variable_map(self):
        if 'custom_variable_map' in self.temp_storage:
            del self.temp_storage['custom_variable_map']

    async def get_custom_variable_map(self) -> Dict:
        if 'custom_variable_map' in self.temp_storage:
            return self.temp_storage['custom_variable_map']

        custom_variable_map = {}
        storage = await self.get_storage()
        for custom_variable in storage.get('custom_variable', []):
            if custom_variable.get('name'):
                custom_variable_map[custom_variable.get('name')] = custom_variable.get('value', '')

        self.temp_storage['custom_variable_map'] = custom_variable_map
        return custom_variable_map

    async def set_tab_index(self, tab_index):
        self.storage['tab_index'] = tab_index

    async def get_storage(self) -> Dict:
        if self.storage is not None:
            return self.storage

        print(f"storage 打开了文件")
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as fp:
                fp.write(json.dumps(INIT_CONFIG_JSON))
        with open(self.storage_path, 'r') as fp:
            self.storage = json.load(fp)

        return self.storage

    async def set_storage(self, storage: Tuple[Dict, str], bak: bool = True):
        if isinstance(storage, str):
            storage_str = storage
        else:
            storage_str = json.dumps(storage)

        self.storage = json.loads(storage_str)
        # self.temp_storage = {}

        if bak:
            file_path = os.path.join(
                self.storage_history_home, f'./{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_bak.json'
            )
            shutil.move(self.storage_path, file_path)
            try:
                if time.time() - self.last_bak_time < 120 and self.last_bak_path:
                    os.remove(self.last_bak_path)
            except Exception:
                pass

            self.last_bak_time = time.time()
            self.last_bak_path = file_path

        with open(self.storage_path, 'w') as fp:
            fp.write(json.dumps(self.storage, sort_keys=True, indent=4))

    async def delete_storage(self):
        file_list = sorted(os.listdir(self.storage_history_home), key=lambda a: a, reverse=True)[120:]
        for file in file_list:
            try:
                os.remove(f'{self.storage_history_home}/{file}')
            except Exception:
                pass


class XPyMethod(object):
    method_map = {}

    def __init__(self, data_list, custom_variable_map):
        __temp_exec = '''
{method_value}

try:
    PY.install('{method_name}',{method_name})
except Exception as e:
    pass
        '''
        for data in data_list:
            try:
                exec(__temp_exec.format(method_name=data.get('name'), method_value=data.get('value')), {
                    'PY': self,
                    'data': custom_variable_map,
                })
            except Exception as e:
                print(f'初始化PyMethod 失败，name:{data.get("name")}，error：{e}')

    def __setattr__(self, key, value):
        self.method_map[key] = value

    def __getattr__(self, item):
        return self.method_map.get(item)

    def install(self, key, value):
        self.method_map[key] = value
