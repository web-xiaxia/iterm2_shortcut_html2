# -*- coding: utf-8 -*-
from typing import Dict, Set

import iterm2
from iterm2 import Connection, App, Window, Tab, Session

from api.py_api import PyApi
from common.session_storage_data import SessionStorageData
from common.storage_data import StorageData


class MonitorHelper:

    def __init__(self, app: App, connection: Connection, session_storage_data: SessionStorageData,
                 storage_data: StorageData, py_api: PyApi):
        self.window_id_to_tab_ids: Dict[str, Set[str]] = {}
        self.tab_id_to_session_ids: Dict[str, Set[str]] = {}
        self.app: App = app
        self.connection: Connection = connection
        self.session_storage_data: SessionStorageData = session_storage_data
        self.storage_data: StorageData = storage_data
        self.py_api: PyApi = py_api
        self.init()

    async def init(self):
        for __w in self.app.terminal_windows:
            await self.init_window(__w)

    async def window_changed(self, window_id: str):
        w = self.app.get_window_by_id(window_id)
        if w:
            await self.init_window(w)

    async def selected_tab_changed(self, tab_id: str):
        t = self.app.get_tab_by_id(tab_id)
        if t:
            await self.init_tab(t)

    async def active_session_changed(self, session_id: str):
        s = self.app.get_session_by_id(session_id)
        if s:
            await self.init_session(s)

    async def init_window(self, w: Window):
        if w.window_id not in self.window_id_to_tab_ids:
            await self.create_window_handler(w.window_id)
            self.window_id_to_tab_ids[w.window_id] = set()

            for t in w.tabs:
                await self.init_tab(t)

        now_window_ids = [fw.window_id for fw in self.app.terminal_windows]
        window_ids = self.window_id_to_tab_ids.copy().keys()
        for wid in window_ids:
            if wid not in now_window_ids:
                del self.window_id_to_tab_ids[wid]
                await self.close_window(wid)

    async def init_tab(self, t: Tab):
        if t.window.window_id not in self.window_id_to_tab_ids:
            await self.init_window(t.window)
        else:
            if t.tab_id not in self.window_id_to_tab_ids[t.window.window_id]:
                await self.create_tab_handler(t.tab_id)
                self.window_id_to_tab_ids[t.window.window_id].add(t.tab_id)
                self.tab_id_to_session_ids[t.tab_id] = set()

                for s in t.sessions:
                    await self.init_session(s)

            now_tab_ids = set([ft.tab_id for ft in t.window.tabs])
            tab_ids = self.window_id_to_tab_ids[t.window.window_id]
            for tid in tab_ids.copy():
                if tid not in now_tab_ids:
                    tab_ids.remove(tid)
                    await self.close_tab(tid)

    async def init_session(self, s: Session):
        if s.tab.tab_id not in self.tab_id_to_session_ids:
            await self.init_tab(s.tab)
        else:
            if s.session_id not in self.tab_id_to_session_ids[s.tab.tab_id]:
                await self.create_session_handler(s.session_id)
                self.tab_id_to_session_ids[s.tab.tab_id].add(s.session_id)

            now_session_ids = set([fs.session_id for fs in s.tab.sessions])
            session_ids = self.tab_id_to_session_ids[s.tab.tab_id]
            for sid in session_ids.copy():
                if sid not in now_session_ids:
                    session_ids.remove(sid)
                    await self.close_session(sid)

    async def close_window(self, wid: str):
        if wid not in self.window_id_to_tab_ids:
            return

        tab_ids = self.window_id_to_tab_ids[wid]
        for tid in tab_ids.copy():
            tab_ids.remove(tid)
            await self.close_tab(tid)

        del self.window_id_to_tab_ids[wid]
        await self.close_window_handler(wid)

    async def close_tab(self, tid: str):
        if tid not in self.tab_id_to_session_ids:
            return

        session_ids = self.tab_id_to_session_ids[tid]
        for sid in session_ids.copy():
            session_ids.remove(sid)
            await self.close_session(sid)

        del self.tab_id_to_session_ids[tid]
        await self.close_tab_handler(tid)

    async def close_session(self, sid: str):
        await self.close_session_handler(sid)

    async def create_window_handler(self, wid: str):
        print(f'create_window_handler:{wid}')

    async def create_tab_handler(self, tid: str):
        print(f'create_tab_handler:{tid},')

    async def create_session_handler(self, sid: str):
        print(f'create_session_handler:{sid},')
        await self.py_api.register_session_auto_trigger(sid)

    async def close_window_handler(self, wid: str):
        print(f'close_window_handler:{wid}')

    async def close_tab_handler(self, tid: str):
        print(f'close_tab_handler:{tid},')

    async def close_session_handler(self, sid: str):
        print(f'close_session_handler:{sid},')
        await self.session_storage_data.delete_storage_by_session_id(sid)


async def register(app: App, connection: Connection,
                   session_storage_data: SessionStorageData, storage_data: StorageData, py_api: PyApi):
    monitor_helper = MonitorHelper(app, connection, session_storage_data, storage_data, py_api)
    async with iterm2.FocusMonitor(connection) as monitor:
        while True:
            update = await monitor.async_get_next_update()
            if update.application_active:
                pass
            elif update.window_changed:
                await monitor_helper.window_changed(update.window_changed.window_id)
            elif update.selected_tab_changed:
                await monitor_helper.selected_tab_changed(update.selected_tab_changed.tab_id)
            elif update.active_session_changed:
                await monitor_helper.active_session_changed(update.active_session_changed.session_id)
