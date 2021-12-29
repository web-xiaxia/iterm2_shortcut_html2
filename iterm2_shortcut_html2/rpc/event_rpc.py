# -*- coding: utf-8 -*-
from api.exec_api import ExecApi
from datetime import time

from api.py_api import PyApi
from rpc import web_view_tool_rpc
from typing import Optional, List

from iterm2.connection import Connection

import iterm2
from common import constants, utils
from common.storage_data import StorageData


async def register(connection: Connection, storage_data: StorageData, http_web_index_url: str, py_api: PyApi,
                   exec_api: ExecApi):
    LAST_OPEN_TOOLBELT_TAB_NAME_TIME = {}

    async def exec_event_name(event_name, params: Optional[List] = None):
        return await exec_api.event_name_exec(event_name, params)

    @iterm2.RPC
    async def shortcut_html_event_feishu(feishu_token: str, title: str, context: str, screen_text_line=0):
        note = None
        if screen_text_line > 0:
            note = await py_api.screen_text(screen_text_line)
        await utils.send_feishu(feishu_token, title, context, note=note)

    await shortcut_html_event_feishu.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_event(event_name: str):
        await shortcut_html_eventx(event_name, [])

    await shortcut_html_event.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_eventx(event_name: str, params: Optional[List[str]] = None):
        await exec_event_name(event_name, params)

    await shortcut_html_eventx.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_send_text(event_name: str):
        await shortcut_html_send_textx(event_name, [])

    await shortcut_html_send_text.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_send_textx(event_name: str, params: Optional[List[str]] = None):
        send_text = await exec_event_name(event_name, params)
        await py_api.send_text(send_text)

    await shortcut_html_send_textx.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_get_text(event_name: str):
        return await shortcut_html_get_textx(event_name, [])

    await shortcut_html_get_text.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_get_textx(event_name: str, params: Optional[List[str]] = None):
        return await exec_event_name(event_name, params)

    await shortcut_html_get_textx.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_open_toolbelt(tab_name):
        now_time = time.time()
        last_time = LAST_OPEN_TOOLBELT_TAB_NAME_TIME.get(tab_name, 0)
        if now_time - last_time < 1:
            return
        LAST_OPEN_TOOLBELT_TAB_NAME_TIME[tab_name] = now_time

        selected_tab = None
        selected_tab_index = None
        storage = await storage_data.get_storage()
        for tab_index, tab in enumerate(storage.get('tabs', [])):
            if tab.get('name') == tab_name:
                selected_tab = tab
                selected_tab_index = tab_index
                break

        if not selected_tab:
            return

        await storage_data.set_tab_index(selected_tab_index)
        print(f'触发打开Toolbelt，index:{selected_tab_index}, tab_name:{tab_name}')

        # 打开 Toolbelt
        menu_item_state = await iterm2.MainMenu.async_get_menu_item_state(connection,
                                                                          constants.SHOW_TOOLBELT_IDENTIFIER)
        if not menu_item_state.checked:
            await iterm2.MainMenu.async_select_menu_item(connection, constants.SHOW_TOOLBELT_IDENTIFIER)

        # 注册 view_tool
        web_view_tool_rpc.register(
            connection, f'{http_web_index_url}?toolbelt_tab_name={tab_name}&time={int(time.time() * 1000)}'
        )

    await shortcut_html_open_toolbelt.async_register(connection)
