# -*- coding: utf-8 -*-
from iterm2.session import Session

from typing import Optional

import traceback
from api.py_api import PyApi
from common.storage_data import StorageData
from iterm2.connection import Connection

from iterm2.app import App

from common.utils import singleton


class Iterm2Api:
    def __init__(self, app: App, connection: Connection):
        self.app: App = app
        self.connection: Connection = connection

    @property
    def session(self) -> Session:
        return self.app.current_terminal_window.current_tab.current_session


@singleton
class ExecApi:
    def __init__(self, app: App, connection: Connection, storage_data: StorageData, py_api: PyApi):
        self.app: App = app
        self.connection: Connection = connection
        self.storage_data: StorageData = storage_data
        self.py_api: PyApi = py_api
        self.iterm2_api: Iterm2Api = Iterm2Api(app, connection)

    async def og_code_exec(self, code: str, params: Optional[list] = None) -> str:
        if not code:
            return ''
        custom_variable_map = await self.storage_data.get_custom_variable_map()
        xpy_method = await self.storage_data.get_xpy_method()
        eval_results = {}

        exec("async def __ex():\n{}\nresults['__ex'] = __ex".format(
            ''.join(f'   {x}\n' for x in code.split('\n'))
        ), {
            'ITERM2': self.iterm2_api,
            'PY': xpy_method,
            'PYX': self.py_api,
            'data': custom_variable_map,
            'params': [] if params is None else params,
            'results': eval_results,
        })
        await eval_results['__ex']()
        return eval_results['event'] if 'event' in eval_results else ''

    async def code_exec(self, code: str, params: Optional[list] = None) -> str:
        try:
            return await self.og_code_exec(code, params)
        except Exception as e:
            print("code_exec 运行失败,{}\n,{}".format(
                e, traceback.format_exc()
            ))
            return ''

    async def event_name_exec(self, event_name: str, params: Optional[list] = None) -> str:
        try:
            selected_event_send = await self.storage_data.get_event_send(event_name)
            if not selected_event_send:
                return ''
            return await self.og_code_exec(selected_event_send.get('value'), params)
        except Exception as e:
            print("event_name_text 获取失败，event_name：{},{}\n,{}".format(
                event_name, e, traceback.format_exc()
            ))
            return ''