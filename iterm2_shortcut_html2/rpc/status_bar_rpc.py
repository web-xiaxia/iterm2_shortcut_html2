# -*- coding: utf-8 -*-
from iterm2.connection import Connection

import iterm2
from common import constants
from common.system_storage_data import SystemStorageHelper


async def register(connection: Connection, system_storage_data: SystemStorageHelper, http_web_index_url: str):
    # 组装组件
    component = iterm2.StatusBarComponent(
        short_description=constants.SHORTCUT_HTML2_NAME,
        detailed_description=constants.SHORTCUT_HTML2_NAME,
        knobs=[],
        exemplar=constants.SHORTCUT_HTML2_NAME,
        update_cadence=None,
        identifier=constants.TOOLBELT_SHORTCUT_IDENTIFIER
    )

    @iterm2.RPC
    async def shortcut_html2_onclick(session_id):
        """
        注册按钮事件
        """
        window_width = 950
        window_height = 480
        try:
            storage = await system_storage_data.get_config()
            window_width = storage.window_width or 950
            window_height = storage.window_height or 480
        except Exception:
            pass

        print(window_width)
        print(window_height)
        await component.async_open_popover(
            session_id,
            f'''
            <html style='background-color: rgb(38, 37, 37);'>
                <script>
                    window.location.href='{http_web_index_url}'
                </script>
                <body style='background-color: rgb(38, 37, 37);'>
                </body>
            </html>
            ''',
            iterm2.util.Size(window_width or 950, window_height or 480)
        )

    @iterm2.StatusBarRPC
    async def shortcut_html2_coro(knobs):
        """
        注册按钮名称
        """
        return ">>> 🖥 <<<"

    # 注册状态栏按钮
    await component.async_register(connection, shortcut_html2_coro, onclick=shortcut_html2_onclick)
