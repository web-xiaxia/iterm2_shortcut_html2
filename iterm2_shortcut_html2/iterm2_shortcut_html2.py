# -*- coding: utf-8 -*-
import time

import traceback
from system_storage import SystemStorage
from typing import List, Optional

from iterm2.connection import Connection
from storage import Storage

import iterm2
import os
from os.path import abspath, dirname

MAIN_HOME = abspath(dirname(__file__))
HTML_HOME = os.path.join(MAIN_HOME, 'html')

SYSTEM_CONFIG = SystemStorage(MAIN_HOME)

STORAGE_DATA: Storage = Storage(SYSTEM_CONFIG)

LAST_OPEN_TOOLBELT_TAB_NAME_TIME = {}


async def main(connection: Connection):
    app = await iterm2.async_get_app(connection)

    @iterm2.RPC
    async def onclick2(session_id):
        window_width = 950
        window_height = 480
        try:
            storage = await STORAGE_DATA.get_storage()
            window_width = storage.get('window_width', 950)
            window_height = storage.get('window_height', 480)
        except Exception:
            pass
        await component.async_open_popover(
            session_id,
            "<html style='background-color: rgb(38, 37, 37);'><script>window.location.href='http://localhost:9998/'</script><body style='background-color: rgb(38, 37, 37);'></body></html>",
            iterm2.util.Size(window_width or 950, window_height or 480)
        )
        # This function gets called whenever any of the paths named in defaults (below) changes
        # or its configuration changes.

    @iterm2.StatusBarRPC
    async def coro2(knobs):
        return ">>> 🖥 <<<"

    component = iterm2.StatusBarComponent(
        short_description="Shortcut html2",
        detailed_description="Shortcut html2",
        knobs=[],
        exemplar="Shortcut html2",
        update_cadence=None,
        identifier="com.iterm2.shortcut-html2")

    # Register the component.
    await component.async_register(connection, coro2, onclick=onclick2)

    # @iterm2.StatusBarRPC
    # async def init_user_variable():
    #     session = app.current_terminal_window.current_tab.current_session
    #     session_json = await STORAGE.get_storage()
    #     for variable in session_json.get('user_variable', []):
    #         await session.async_set_variable(
    #             f'user.{variable.get("name")}',
    #             variable.get('value').replace('\r', '').replace('\n', '').replace('%0a', '')
    #         )

    async def event_name_text(event_name, params: Optional[List[str]] = None):
        try:
            selected_event_send = await STORAGE_DATA.get_event_send(event_name)
            if not selected_event_send:
                return
            custom_variable_map = await STORAGE_DATA.get_custom_variable_map()
            xpy_method = await STORAGE_DATA.get_xpy_method()
            eval_results = {}
            exec(selected_event_send.get('value'), {
                'PY': xpy_method,
                'data': custom_variable_map,
                'params': [] if params is None else params,
                'results': eval_results,
            })
            return eval_results['event'] if 'event' in eval_results else ''
        except Exception as e:
            print(f"event_name_text 获取失败，{event_name:},{e}\n,{traceback.format_exc()}")
            return ''

    @iterm2.RPC
    async def shortcut_html_send_text(event_name: str):
        await shortcut_html_send_textx(event_name, [])

    await shortcut_html_send_text.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_send_textx(event_name: str, params: Optional[List[str]] = None):
        send_text = await event_name_text(event_name, params)
        if send_text:
            session = app.current_terminal_window.current_tab.current_session
            await session.async_send_text(send_text.replace('|==f==h==|', '"'))

    await shortcut_html_send_textx.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_get_text(event_name: str):
        return await shortcut_html_get_textx(event_name, [])

    await shortcut_html_get_text.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_get_textx(event_name: str, params: Optional[List[str]] = None):
        return await event_name_text(event_name, params)

    await shortcut_html_get_textx.async_register(connection)

    @iterm2.RPC
    async def shortcut_html_open_toolbelt(tab_name):
        now_time = time.time()
        last_time = LAST_OPEN_TOOLBELT_TAB_NAME_TIME.get(tab_name, 0)
        if now_time - last_time < 1:
            return
        LAST_OPEN_TOOLBELT_TAB_NAME_TIME[tab_name] = now_time

        print(f"触发打开Toolbelt,{tab_name:}")
        menu_item_name = 'Show Toolbelt'
        menu_item_state = await iterm2.MainMenu.async_get_menu_item_state(connection, menu_item_name)
        menu_item_state_checked = menu_item_state.checked

        selected_tab = None
        selected_tab_index = None
        storage = await STORAGE_DATA.get_storage()
        for tab_index, tab in enumerate(storage.get('tabs', [])):
            if tab.get('name') == tab_name:
                selected_tab = tab
                selected_tab_index = tab_index
                break
        if not selected_tab:
            return

        await STORAGE_DATA.set_tab_index(selected_tab_index)

        await iterm2.MainMenu.async_select_menu_item(connection, menu_item_name)
        if menu_item_state_checked:
            print(f"二次触发打开Toolbelt,{tab_name:}")
            await iterm2.MainMenu.async_select_menu_item(connection, menu_item_name)

    await shortcut_html_open_toolbelt.async_register(connection)

    #
    # @iterm2.RPC
    # async def vim_mode():
    #     send_text = await event_name_text('vim_mode')
    #     if send_text:
    #         session = app.current_terminal_window.current_tab.current_session
    #         await session.async_send_text(send_text.replace('|==f==h==|', '"'))
    #
    #     await open_tool_belt(o=1, key='vim')
    #
    # await vim_mode.async_register(connection)

    # 注册web
    from html_api import api_register
    await api_register(connection, app, SYSTEM_CONFIG, STORAGE_DATA, MAIN_HOME, HTML_HOME)


iterm2.run_forever(main)
