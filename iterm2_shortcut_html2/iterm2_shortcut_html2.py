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

SHORTCUT_HTML2_NAME = 'Shortcut html2'
SHOW_TOOLBELT_IDENTIFIER = 'Show Toolbelt'
TOOLBELT_SHORTCUT_HTML1_IDENTIFIER = 'com.iterm2.toolbelt.shortcut-html2'


async def main(connection: Connection):
    app = await iterm2.async_get_app(connection)

    @iterm2.RPC
    async def shortcut_html2_onclick(session_id):
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

    @iterm2.StatusBarRPC
    async def shortcut_html2_coro(knobs):
        return ">>> 🖥 <<<"

    component = iterm2.StatusBarComponent(
        short_description=SHORTCUT_HTML2_NAME,
        detailed_description=SHORTCUT_HTML2_NAME,
        knobs=[],
        exemplar=SHORTCUT_HTML2_NAME,
        update_cadence=None,
        identifier="com.iterm2.shortcut-html2"
    )
    # 注册状态栏按钮
    await component.async_register(connection, shortcut_html2_coro, onclick=shortcut_html2_onclick)

    # 注册toolbelt
    await iterm2.tool.async_register_web_view_tool(
        connection, SHORTCUT_HTML2_NAME, TOOLBELT_SHORTCUT_HTML1_IDENTIFIER, False,
        "http://localhost:9998/"
    )

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
            print("event_name_text 获取失败，event_name：{},{}\n,{}".format(
                event_name, e, traceback.format_exc()
            ))
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
        print(f'触发打开Toolbelt，index:{selected_tab_index}, tab_name:{tab_name}')

        # 打开 Toolbelt
        menu_item_state = await iterm2.MainMenu.async_get_menu_item_state(connection, SHOW_TOOLBELT_IDENTIFIER)
        if not menu_item_state.checked:
            await iterm2.MainMenu.async_select_menu_item(connection, SHOW_TOOLBELT_IDENTIFIER)

        await iterm2.tool.async_register_web_view_tool(
            connection, 'Shortcut html2', TOOLBELT_SHORTCUT_HTML1_IDENTIFIER, False,
            f"http://localhost:9998?toolbelt_tab_name={tab_name}&time={int(time.time() * 1000)}"
        )

    await shortcut_html_open_toolbelt.async_register(connection)

    # 注册web
    from html_api import api_register
    await api_register(connection, app, SYSTEM_CONFIG, STORAGE_DATA, MAIN_HOME, HTML_HOME)


iterm2.run_forever(main)
