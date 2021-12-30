# -*- coding: utf-8 -*-
from api.exec_api import ExecApi
from iterm2.app import App

from api import html_api
from api.py_api import PyApi
from common.session_storage_data import SessionStorageData
from common.system_storage_data import SystemStorageData

from rpc import status_bar_rpc, web_view_tool_rpc, event_rpc

from iterm2.connection import Connection
from common.storage_data import StorageData

import iterm2
import os
from os.path import abspath, dirname


async def main(connection: Connection):
    # 定义工作目录
    app: App = await iterm2.async_get_app(connection)
    main_home = abspath(dirname(__file__))
    html_home = os.path.join(main_home, 'html')
    # 存储信息
    system_storage_data: SystemStorageData = SystemStorageData(main_home)
    storage_data: StorageData = StorageData(system_storage_data)
    session_storage_data: SessionStorageData = SessionStorageData(app)
    #
    py_api: PyApi = PyApi(app, connection)
    exec_api: ExecApi = ExecApi(app, connection, session_storage_data, storage_data, py_api)
    http_web_host = 'localhost'
    http_web_port = 9998
    http_web_index_url = f"http://{http_web_host}:{http_web_port}/"

    # 注册状态栏
    await status_bar_rpc.register(connection, storage_data, http_web_index_url)
    # 注册view_tool
    await web_view_tool_rpc.register(connection, http_web_index_url)
    # 注册事件
    await event_rpc.register(connection, storage_data, http_web_index_url, py_api, exec_api)
    # 注册web
    await html_api.register(
        system_storage_data, session_storage_data, storage_data, py_api, exec_api,
        main_home, html_home, http_web_host, http_web_port
    )


iterm2.run_forever(main)
