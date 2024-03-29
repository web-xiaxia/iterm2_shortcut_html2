# -*- coding: utf-8 -*-
import time

from datetime import datetime
from common.system_storage_data import SystemStorageData
from common.utils import singleton

import shutil
from typing import Dict, Tuple, Optional, List
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


@singleton
class StorageData:

    def __init__(self, system_storage_data: SystemStorageData):
        self.system_storage_data = system_storage_data
        self.storage = None
        self.temp_storage = {}
        self.last_bak_time = 0
        self.last_bak_path = None
        self.storage_file_name = 'storage.json'

    async def reset_xpy_method(self):
        if 'py_method' in self.temp_storage:
            del self.temp_storage['py_method']

    async def get_xpy_method(self) -> 'XPyMethod':
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

    async def set_custom_variable(self, key, value):
        if (not isinstance(value, str)
                and not isinstance(value, bool)
                and not isinstance(value, float)
                and not isinstance(value, int)):
            return
        saved = False
        storage = await self.get_storage()
        if 'custom_variable' not in storage:
            storage['custom_variable'] = []
        for custom_variable in storage.get('custom_variable', []):
            if custom_variable.get('name') == key:
                custom_variable['value'] = value
                saved = True
                break
        if not saved:
            storage['custom_variable'].append({
                'name': key,
                'value': value,
            })
        await self.set_storage(None, bak=False)

    async def get_custom_variable_map(self) -> 'CustomVariable':
        if 'custom_variable_map' in self.temp_storage:
            return self.temp_storage['custom_variable_map']

        custom_variable_map = dict()
        storage = await self.get_storage()
        for custom_variable in storage.get('custom_variable', []):
            if custom_variable.get('name'):
                custom_variable_map[custom_variable.get('name')] = custom_variable.get('value', '')

        self.temp_storage['custom_variable_map'] = CustomVariable(custom_variable_map, self)
        return self.temp_storage['custom_variable_map']

    async def get_custom_trigger(self, trigger_name) -> Optional[Dict]:
        storage = await self.get_storage()
        for custom_trigger in storage.get('custom_trigger', []):
            if custom_trigger.get('name') == trigger_name:
                return custom_trigger
        return None

    async def get_session_auto_custom_trigger(self) -> List[Dict]:
        storage = await self.get_storage()
        session_auto_custom_trigger_list = []
        for custom_trigger in storage.get('custom_trigger', []):
            if custom_trigger.get('auto'):
                session_auto_custom_trigger_list.append(custom_trigger)
        return session_auto_custom_trigger_list

    async def set_toolbelt_tab_index(self, tab_index):
        self.storage['toolbelt_tab_index'] = tab_index

    async def get_storage(self) -> Dict:
        if self.storage is not None:
            return self.storage

        print(f"storage 打开了文件")
        system_config_storage = await self.system_storage_data.get_storage()
        storage_full_path = os.path.join(system_config_storage.get('storage_path'), self.storage_file_name)
        if not os.path.exists(storage_full_path):
            with open(storage_full_path, 'w') as fp:
                fp.write(json.dumps(INIT_CONFIG_JSON))
        with open(storage_full_path, 'r') as fp:
            self.storage = json.load(fp)

        return self.storage

    async def reload_storage(self, path):
        if not path:
            system_config_storage = await self.system_storage_data.get_storage()
            path = os.path.join(system_config_storage.get('storage_path'), self.storage_file_name)

        if not os.path.exists(path):
            with open(path, 'w') as fp:
                fp.write(json.dumps(INIT_CONFIG_JSON))
        if not os.path.isfile(path):
            return
        with open(path, 'r') as fp:
            self.storage = json.load(fp)
        await self.set_storage(self.storage, bak=True)

    async def set_storage(self, storage: Optional[Tuple[Dict, str]], bak: bool = True):
        if storage is not None:
            if isinstance(storage, str):
                storage_str = storage
            else:
                storage_str = json.dumps(storage)
            self.storage = json.loads(storage_str)

        system_config_storage = await self.system_storage_data.get_storage()
        storage_full_path = os.path.join(system_config_storage.get('storage_path'), self.storage_file_name)
        if bak:
            storage_history_home = system_config_storage.get('storage_history_path')
            file_path = os.path.join(
                storage_history_home, f'./{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_bak.json'
            )

            shutil.move(storage_full_path, file_path)
            try:
                if time.time() - self.last_bak_time < 120 and self.last_bak_path:
                    os.remove(self.last_bak_path)
            except Exception:
                pass

            self.last_bak_time = time.time()
            self.last_bak_path = file_path

        with open(storage_full_path, 'w') as fp:
            fp.write(json.dumps(self.storage, sort_keys=True, indent=4))

    async def delete_storage(self):
        system_config_storage = await self.system_storage_data.get_storage()
        storage_history_home = system_config_storage.get('storage_history_path')
        file_list = sorted(os.listdir(storage_history_home), key=lambda a: a, reverse=True)[120:]
        for file in file_list:
            if file == self.storage_file_name:
                continue
            try:
                os.remove(f'{storage_history_home}/{file}')
            except Exception:
                pass


class XPyMethod(object):
    method_map_data = None

    def __init__(self, data_list, custom_variable_map):
        super().__setattr__('method_map_data', dict())
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

    def __getattr__(self, item):
        return super().__getattribute__('method_map_data').get(item)

    def install(self, key, value):
        super().__getattribute__('method_map_data')[key] = value


class CustomVariable(object):
    storage_data: StorageData = None
    storage = None

    def __init__(self, storage: Dict, storage_data: StorageData):
        super().__setattr__('storage_data', storage_data)
        super().__setattr__('storage', storage)

    def __setattr__(self, key, value):
        super().__getattribute__('storage_data').set_custom_variable(key, value)

    def __getattr__(self, item):
        return super().__getattribute__('storage').get(item)

    def __setitem__(self, key, value):
        super().__getattribute__('storage_data').set_custom_variable(key, value)

    def __getitem__(self, item):
        return super().__getattribute__('storage').get(item)

    def get(self, key, default=None):
        return super().__getattribute__('storage').get(key, default)
