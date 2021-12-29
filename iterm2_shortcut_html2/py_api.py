# -*- coding: utf-8 -*-
from typing import Dict
from iterm2.connection import Connection

from iterm2.app import App
import utils
from utils import singleton


@singleton
class PyApi:
    def __init__(self, app: App, connection: Connection):
        self.app = app
        self.connection = connection

    async def send_text(self, send_text_context):
        utils.send_text(self.app, send_text_context)

    async def alert(self, title='', subtitle=''):
        await utils.alert(self.connection, title=title, subtitle=subtitle)

    async def confirm(self, title='', subtitle='', buttons=None) -> int:
        if not buttons:
            buttons = ['ok', 'cancel']
        return await utils.alert(self.connection, title=title, subtitle=subtitle, buttons=buttons)

    async def prompt(self, title='', subtitle='', placeholder='', default_value='') -> str:
        return await utils.prompt(title, subtitle, placeholder, default_value)

    async def send_http(self, url, method, headers=None, params=None, data=None, json_data=None) -> Dict:
        return utils.send_http(url, method, headers, params, data, json_data)

    async def screen_text(self, number_of_lines=30) -> str:
        if number_of_lines < 1:
            number_of_lines = 1
        session = self.app.current_terminal_window.current_tab.current_session
        line_info = await session.async_get_line_info()
        if line_info.scrollback_buffer_height < 1:
            line_start = 0
            line_end = line_info.mutable_area_height - 1
            line_contents = await session.async_get_contents(line_start, line_end)
            line_contents = [line_content for line_content in line_contents if line_content.string][-number_of_lines:]
        else:
            line_end = line_info.overflow + line_info.scrollback_buffer_height + line_info.mutable_area_height - 2
            line_start = line_end - (number_of_lines - 1)
            if line_start < 0:
                line_start = 0
            line_contents = await session.async_get_contents(line_start, line_end)
            line_contents = line_contents[0: number_of_lines]

        # print(
        #     f'{line_info.mutable_area_height},'
        #     f'{line_info.scrollback_buffer_height},'
        #     f'{line_info.overflow},'
        #     f'{line_info.first_visible_line_number},'
        #     f'{line_start},{line_end}')
        line_content_array = [line_content.string for line_content in line_contents]
        return '\n'.join(line_content_array)

    async def send_feishu(self, token: str, title: str, context: str, note: str = None):
        await utils.send_feishu(token, title, context, note)
