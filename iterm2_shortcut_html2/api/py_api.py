# -*- coding: utf-8 -*-
import os
import subprocess
import traceback

import iterm2
import json
from typing import Dict, Optional, Tuple, List
from iterm2.connection import Connection

from iterm2.app import App
from common import utils
from common.storage_data import StorageData
from common.utils import singleton


@singleton
class PyApi:
    def __init__(self, app: App, connection: Connection, storage_data: StorageData, osascript_home: str):
        self.app: App = app
        self.connection: Connection = connection
        self.storage_data: StorageData = storage_data
        self.osascript_home: str = osascript_home

    async def __send_text(self, app, send_text_context: str, run_type=""):
        if send_text_context:
            if run_type == 'warp':
                warp_path = os.path.join( self.osascript_home, 'warp.scpt')
                warp_send_text_context = send_text_context.replace("\\","\\\\").replace("\"","\\\"")
                cmd = f'osascript {warp_path} "{warp_send_text_context}"'
                print(cmd)
                os.system(cmd)
            else:
                session = app.current_terminal_window.current_tab.current_session
                await session.async_send_text(send_text_context)

    async def __alert(self, connection: Connection, title='', subtitle='', buttons=None) -> int:
        if not buttons:
            buttons = []
        title = json.dumps(title, ensure_ascii=False)
        subtitle = json.dumps(subtitle, ensure_ascii=False)
        buttons = json.dumps(buttons, ensure_ascii=False)

        return await iterm2.async_invoke_function(
            connection,
            (f'iterm2.alert(title: {title}, ' +
             f'subtitle: {subtitle}, ' +
             f'buttons: {buttons}, ' +
             f'window_id: {json.dumps(None)})'))

    async def __prompt(self, connection: Connection, title='', subtitle='', placeholder='',
                       default_value='') -> Optional[str]:
        title = json.dumps(title, ensure_ascii=False)
        subtitle = json.dumps(subtitle, ensure_ascii=False)
        placeholder = json.dumps(placeholder, ensure_ascii=False)
        default_value = json.dumps(default_value, ensure_ascii=False)
        return await iterm2.async_invoke_function(
            connection,
            (f'iterm2.get_string(title: {title}, ' +
             f'subtitle: {subtitle}, ' +
             f'placeholder: {placeholder}, ' +
             f'defaultValue: {default_value}, ' +
             f'window_id: {json.dumps(None)})'))

    async def send_text(self, send_text_context, run_type=""):
        await self.__send_text(self.app, send_text_context,run_type)

    async def send_hex_code(self, send_hex_code: str):
        session = self.app.current_terminal_window.current_tab.current_session
        # https://iterm2.com/documentation-escape-codes.html
        await session.async_inject(b'\x1b' + b']' + bytes(str(send_hex_code), encoding="utf-8") + b'\x07')

    async def selected_text(self):
        session = self.app.current_terminal_window.current_tab.current_session
        selection = await session.async_get_selection()

        return await session.async_get_selection_text(selection)

    async def exec_shell(self, shell_text: str) -> Tuple[bool, List[str]]:
        p = subprocess.Popen(shell_text, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
        while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
            if p.wait() != 0:  # 判断是否执行成功（Popen.wait()等待子进程结束，并返回状态码；如果设置并且在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。）
                print("命令执行失败，请检查设备连接状态")
                return False, []
            else:
                shell_result = p.stdout.readlines()  # 获取原始执行结果
                result = []
                for i in range(len(shell_result)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
                    res = shell_result[i].decode('utf-8').strip('\r\n')
                    result.append(res)
                return True, result

    async def alert(self, title='', subtitle=''):
        await self.__alert(self.connection, title=title, subtitle=subtitle)

    async def confirm(self, title='', subtitle='', buttons=None) -> int:
        if not buttons:
            buttons = ['ok', 'cancel']
        return await self.__alert(self.connection, title=title, subtitle=subtitle, buttons=buttons)

    async def prompt(self, title='', subtitle='', placeholder='', default_value='') -> Optional[str]:
        return await self.__prompt(self.connection, title, subtitle, placeholder, default_value)

    async def send_http(self, url, method, headers=None, params=None, data=None, json_data=None) -> Dict:
        return await utils.send_http(url, method, headers, params, data, json_data)

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

    async def get_triggers(self):
        session = self.app.current_terminal_window.current_tab.current_session
        profile = await session.async_get_profile()
        triggers = []
        for trigger in profile.triggers:
            try:
                # regex
                # action
                # parameter
                # partial
                # disabled
                print(f'{json.dumps(trigger)}')
                triggers.append(iterm2.decode_trigger(trigger))
            except Exception as e:
                print(f'trigger decode error:{e}\n{json.dumps(trigger)}\n{traceback.format_exc()}')

        return triggers

    async def get_trigger_encode(self, custom_trigger):
        if not custom_trigger:
            return None
        if custom_trigger.get('action') == 'iTermRPCTrigger':
            return iterm2.RPCTrigger(
                regex=custom_trigger.get('regex'),
                invocation=custom_trigger.get('parameter'),
                instant=custom_trigger.get('partial'),
                enabled=True
            ).encode

        return None

    async def get_custom_trigger_encode(self, trigger_name: str) -> Optional[Dict]:
        custom_trigger = await self.storage_data.get_custom_trigger(trigger_name)

        return await self.get_trigger_encode(custom_trigger)

    async def trigger_encode_md5(self, trigger: Dict) -> str:
        trigger_kv_str_list = ['{}:{}'.format(k, v) for k, v in trigger.items()]
        trigger_kv_str_list.sort(key=lambda a: a)
        return await utils.md5('|'.join(trigger_kv_str_list))

    async def register_trigger(self, trigger_name: str):
        custom_trigger_encode = await self.get_custom_trigger_encode(trigger_name)
        if not custom_trigger_encode:
            print(f'未找到trigger：{trigger_name}')
            return

        custom_trigger_encode_md5 = await self.trigger_encode_md5(custom_trigger_encode)

        session = self.app.current_terminal_window.current_tab.current_session
        profile = await session.async_get_profile()
        triggers = profile.triggers
        for trigger in triggers:
            if await self.trigger_encode_md5(trigger) == custom_trigger_encode_md5:
                return

        triggers.append(custom_trigger_encode)
        await profile.async_set_triggers(profile.triggers)

    async def register_session_auto_trigger(self, sid: str):
        session = self.app.get_session_by_id(sid)
        if not session:
            return

        session_auto_custom_trigger_list = await self.storage_data.get_session_auto_custom_trigger()
        if not session_auto_custom_trigger_list:
            return

        profile = await session.async_get_profile()
        triggers = profile.triggers
        has_trigger_md5_set = set()
        for trigger in triggers:
            trigger_md5 = await self.trigger_encode_md5(trigger)
            has_trigger_md5_set.add(trigger_md5)

        has_add = False
        for session_auto_custom_trigger in session_auto_custom_trigger_list:
            custom_trigger_encode = await self.get_trigger_encode(session_auto_custom_trigger)
            if custom_trigger_encode:
                trigger_md5 = await self.trigger_encode_md5(custom_trigger_encode)
                if trigger_md5 not in has_trigger_md5_set:
                    triggers.append(custom_trigger_encode)
                    has_add = True
        if has_add:
            await profile.async_set_triggers(profile.triggers)
