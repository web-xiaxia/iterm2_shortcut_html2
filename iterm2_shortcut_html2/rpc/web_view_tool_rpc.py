# -*- coding: utf-8 -*-
from iterm2.connection import Connection

import iterm2
from common import constants


async def register(connection: Connection, http_web_index_url: str):
    # 注册toolbelt
    await iterm2.tool.async_register_web_view_tool(
        connection, constants.SHORTCUT_HTML2_NAME, constants.TOOLBELT_SHORTCUT_HTML1_IDENTIFIER, False,
        http_web_index_url
    )
