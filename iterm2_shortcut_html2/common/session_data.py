# -*- coding: utf-8 -*-
from iterm2 import App
from common.utils import singleton


@singleton
class SessionStorageData:

    def __init__(self, app: App):
        self.app = app
        self.storage = {}

    async def get_storage(self):
        session_id = self.app.current_window.current_tab.current_session.session_id
        if session_id not in self.storage:
            self.storage[session_id] = SessionStorage()
        return self.storage

    async def delete_storage(self):
        session_id = self.app.current_window.current_tab.current_session.session_id
        if session_id in self.storage:
            del self.storage[session_id]

    async def set_storage(self, key: str, value: object):
        storage = await self.get_storage()
        storage[key] = value


class SessionStorage:
    def __init__(self):
        self.storage = {}

    def __setattr__(self, key, value):
        self.storage[key] = value

    def __getattr__(self, item):
        return self.storage.get(item)
