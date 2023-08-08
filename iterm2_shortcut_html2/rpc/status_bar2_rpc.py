# -*- coding: utf-8 -*-
from iterm2.connection import Connection

import iterm2
from common import constants
from common.storage_data import StorageData


async def register(connection: Connection, storage_data: StorageData,
    http_web_index_url: str):
    # 组装组件
    component2 = iterm2.StatusBarComponent(
        short_description=constants.SHORTCUT_HTML2_JSON_NAME,
        detailed_description=constants.SHORTCUT_HTML2_JSON_NAME,
        knobs=[],
        exemplar=constants.SHORTCUT_HTML2_JSON_NAME,
        update_cadence=None,
        identifier=constants.TOOLBELT_SHORTCUT_IDENTIFIER2
    )

    @iterm2.RPC
    async def shortcut_html2_onclick2(session_id):
        """
        注册按钮事件
        """
        window_width = 950
        window_height = 480
        try:
            storage = await storage_data.get_storage()
            window_width = storage.get('window_width', 950)
            window_height = storage.get('window_height', 480)
        except Exception:
            pass
        await component2.async_open_popover(
            session_id,
            f'''
                <html style='background-color: rgb(38, 37, 37);'>
                    <script>
                        window.location.href='{http_web_index_url}?json=1'
                    </script>
                    <body style='background-color: rgb(38, 37, 37);'>
                    </body>
                </html>
                ''',
            iterm2.util.Size(window_width or 950, window_height or 480)
        )

    @iterm2.StatusBarRPC
    async def shortcut_html2_coro2(knobs):
        """
        注册按钮名称
        """
        return "🆒JSON"

    # 注册状态栏按钮
    await component2.async_register(connection, shortcut_html2_coro2,
                                    onclick=shortcut_html2_onclick2)
