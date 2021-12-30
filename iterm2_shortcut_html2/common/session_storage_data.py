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
        return self.storage[session_id]

    async def delete_storage(self):
        session_id = self.app.current_window.current_tab.current_session.session_id
        if session_id in self.storage:
            del self.storage[session_id]

    async def set_storage(self, key: str, value: object):
        storage = await self.get_storage()
        storage[key] = value


class SessionStorage(object):
    storage = None

    def __init__(self):
        super().__setattr__('storage', dict())

    def __setattr__(self, key, value):
        super().__getattribute__('storage')[key] = value
        print(f"SessionStorageLen:{len(super().__getattribute__('storage'))}")

    def __getattr__(self, item):
        return super().__getattribute__('storage').get(item)

    def __setitem__(self, key, value):
        super().__getattribute__('storage')[key] = value
        print(f"SessionStorageLen:{len(super().__getattribute__('storage'))}")

    def __getitem__(self, item):
        return super().__getattribute__('storage').get(item)
