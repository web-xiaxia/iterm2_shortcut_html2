# -*- coding: utf-8 -*-
from iterm2.connection import Connection

from iterm2.app import App
import utils
from utils import singleton


@singleton
class PyApi:
    def __init__(self, app: App, connection: Connection):
        self.app = app
        self.connection = connection

    async def send_text(self, send_text):
        if send_text:
            session = self.app.current_terminal_window.current_tab.current_session
            await session.async_send_text(send_text.replace('|==f==h==|', '"'))

    async def alert(self, title='', subtitle=''):
        await utils.alert(self.connection, title=title, subtitle=subtitle)

    async def confirm(self, title='', subtitle='', buttons=None):
        if not buttons:
            buttons = ['ok', 'cancel']
        return await utils.alert(self.connection, title=title, subtitle=subtitle, buttons=buttons)

    async def prompt(self, title='', subtitle='', placeholder='', default_value='', ):
        return await utils.prompt(title, subtitle, placeholder, default_value)

    async def send_http(self, url, method, headers: None, params: None, data: None, json_data: None):
        return utils.send_http(url, method, headers, params, data, json_data)
