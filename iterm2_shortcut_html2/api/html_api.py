# -*- coding: utf-8 -*-
from api.exec_api import ExecApi
from api.py_api import PyApi
import re

import sqlite3
from common import utils
from common.session_data import SessionStorageData
from common.system_storage_data import SystemStorageData
from common.storage_data import StorageData
from typing import Tuple, List

import json
import os

from aiohttp import web

CONTEXT_INCLUDE_PATTERN = re.compile(r'''(<context-include src=["|'](.*?)["|']/>)''')
HTML_INCLUDE_PATTERN = re.compile(r'''(<html-include src=["|'](.*?)["|']/>)''')
BLOCK_STYLE_PATTERN = re.compile(r'''{% block style %}(.*?){% endblock %}''', re.DOTALL)
BLOCK_SCRIPT_PATTERN = re.compile(r'''{% block script %}(.*?){% endblock %}''', re.DOTALL)
BLOCK_CONTEXT_PATTERN = re.compile(r'''{% block context %}(.*?){% endblock %}''', re.DOTALL)


async def register(system_storage_data: SystemStorageData, session_storage_data: SessionStorageData,
                   storage_data: StorageData, py_api: PyApi, exec_api: ExecApi,
                   main_home: str, html_home: str, http_web_host: str, http_web_port: int):
    async def include_block(html: str) -> Tuple[List[str], List[str], List[str]]:
        style_block = BLOCK_STYLE_PATTERN.findall(html)
        script_block = BLOCK_SCRIPT_PATTERN.findall(html)
        context_block = BLOCK_CONTEXT_PATTERN.findall(html)

        return style_block, script_block, context_block

    async def include_html_util(html_text: str) -> str:
        html_text_return = html_text
        for include_html, include_html_path in CONTEXT_INCLUDE_PATTERN.findall(html_text):
            with open(os.path.join(html_home, include_html_path), 'r') as fp:
                html_text_return = html_text_return.replace(include_html, fp.read())

        has_include_html_path = set()
        style_block_list = []
        script_block_list = []
        context_block_list = []
        for include_html, include_html_path in HTML_INCLUDE_PATTERN.findall(html_text):
            if include_html_path not in has_include_html_path:
                with open(os.path.join(html_home, include_html_path), 'r') as fp:
                    html_text_return = html_text_return.replace(include_html, "")
                    style_block, script_block, context_block = await include_block(fp.read())
                    style_block_list += style_block
                    script_block_list += script_block
                    context_block_list += context_block

        html_text_return = html_text_return.replace('{% block style %}{% endblock %}', '\n'.join(style_block_list))
        html_text_return = html_text_return.replace('{% block script %}{% endblock %}', '\n'.join(script_block_list))
        html_text_return = html_text_return.replace('{% block context %}{% endblock %}', '\n'.join(context_block_list))
        return html_text_return

    async def send_html(txt, request, content_type='application/json; charset=utf-8'):
        binary = txt.encode('utf8')
        resp = web.StreamResponse()
        resp.content_length = len(binary)
        resp.content_type = content_type
        await resp.prepare(request)
        await resp.write(binary)
        return resp

    async def send_error(request, message=''):
        return await send_html(json.dumps({'status': False, 'message': message}), request)

    async def send_ok(request):
        return await send_html(json.dumps({'status': True}), request)

    async def main_page(request):
        with open(os.path.join(html_home, './index.html'), 'r') as fp:
            html_text = fp.read()
            return await send_html(await include_html_util(html_text), request, content_type='text/html')

    async def get_storage_api(request):
        try:
            return await send_html(json.dumps(await storage_data.get_storage(), sort_keys=True, indent=4), request)
        except Exception:
            return await send_html("{}", request)

    async def save_storage_api(request):
        data = await request.json()
        storage_data_version_id = data.get('storage_data_version_id')
        new_storage = data.get('storage')
        bak = data.get('bak')
        if bak:
            print(f"{new_storage.get('storage_data_version_id')} , {storage_data_version_id}")

        storage = await storage_data.get_storage()
        if storage_data_version_id != storage.get('storage_data_version_id'):
            return await send_error(request, "保存失败，请刷新或重新打开页面")

        await storage_data.set_storage(new_storage, bak=bak)
        return await send_ok(request)

    async def delete_storage_api(request):
        await storage_data.delete_storage()
        return await send_ok(request)

    async def reload_storage_api(request):
        data = await request.json()
        path = data.get('path')
        await storage_data.reload_storage(path)
        return await send_ok(request)

    async def save_session_storage_api(request):
        data = await request.json()
        key = data.get('key')
        value = data.get('value')
        await session_storage_data.set_storage(key, value)
        return await send_ok(request)

    async def get_system_storage_api(request):
        return await send_html(json.dumps(await system_storage_data.get_storage(), sort_keys=True, indent=4), request)

    async def save_store_path_api(request):
        data = await request.json()
        storage_path = data.get('storage_path')
        storage_history_path = data.get('storage_history_path')
        reload = bool(data.get('reload'))
        await system_storage_data.set_storage_path(storage_path, storage_history_path)
        if storage_path:
            if reload:
                await storage_data.reload_storage(storage_path + "/storage.json")
            else:
                await storage_data.set_storage(None, bak=True)
        return await send_ok(request)

    async def storage_reset_event_send_map_api(request):
        await storage_data.reset_event_send_map()
        return await send_ok(request)

    async def storage_reset_custom_variable_map_api(request):
        await storage_data.reset_custom_variable_map()
        return await send_ok(request)

    async def storage_reset_py_method_api(request):
        await storage_data.reset_xpy_method()
        return await send_ok(request)

    async def proxy_api(request):
        request_data = await request.json()
        url = request_data.get('url')
        method = request_data.get('method')
        headers = request_data.get('headers')
        params = request_data.get('params', None)
        data = request_data.get('data', None)
        json_data = request_data.get('json_data', None)

        r = await utils.send_http(url, method, headers, params, data, json_data)
        return await send_html(json.dumps(r), request)

    async def send_text_api(request):
        data = await request.post()
        send_text_context = data['send_text']
        await py_api.send_text(send_text_context)
        return await send_ok(request)

    async def send_hex_code_api(request):
        data = await request.post()
        await py_api.send_hex_code(data['send_hex_code'])
        return await send_ok(request)

    async def exec_shell_api(request):
        data = await request.post()
        shell_text = data['shell']
        status, result = await py_api.exec_shell(shell_text)

        return await send_html(json.dumps({
            'status': status,
            'result': result,
        }), request)

    async def selected_text_api(request):
        selected_text = await py_api.selected_text()
        return await send_html(json.dumps({
            'selected_text': selected_text,
        }), request)

    async def path_file_api(request):
        data = await request.post()
        dir_path = data['dir_path']
        select_mode = data['select_mode']
        try:
            file_list = []
            for file in sorted(os.listdir(dir_path), key=lambda a: a):
                isdir = os.path.isdir(f'{dir_path}/{file}')
                isfile = os.path.isfile(f'{dir_path}/{file}')
                if isdir or (isfile and select_mode in ['all', 'file']):
                    file_list.append({
                        'name': file,
                        'isdir': isdir
                    })

            return await send_html(json.dumps({
                'status': True,
                'dir_info': {
                    'root': dir_path,
                    'files': file_list
                },
            }), request)
        except Exception as e:
            return await send_html(json.dumps({
                'status': False,
                'message': "{}".format(e),
            }), request)

    async def iterm2_alert_api(request):
        data = await request.post()
        title = data['title']
        subtitle = data['subtitle']
        await py_api.alert(title=title, subtitle=subtitle)
        return await send_ok(request)

    async def iterm2_confirm_api(request):
        data = await request.json()
        title = data['title']
        subtitle = data['subtitle']
        buttons = data['buttons']
        return await send_html(json.dumps({
            'status': await py_api.confirm(title=title, subtitle=subtitle, buttons=buttons)
        }), request)

    async def iterm2_prompt_api(request):
        data = await request.json()
        title = data['title']
        subtitle = data['subtitle']
        default_value = data['default_value']
        return await send_html(json.dumps({
            'status': await py_api.prompt(title, subtitle, '', default_value)
        }), request)

    async def test_event_name_api(request):
        data = await request.json()
        event_name = data['event_name']
        params = data.get('params', [])
        status, data, message = await exec_api.test_event_name_exec(event_name, params)
        return await send_html(json.dumps({
            'status': status,
            'data': data,
            'message': message,
        }), request)

    async def restart_api(_):
        os.system(
            "ps -ef | grep python | grep -v grep | grep iterm2_shortcut_html2.py | awk '{print $2}' | xargs kill -9  "
            "&& nohup /bin/bash /Applications/iTerm.app/Contents/Resources/it2_api_wrapper.sh "
            + os.path.join(main_home, '../iterm2env/versions/3.7.9/bin/python3 ')
            + main_home + "/iterm2_shortcut_html2.py 2>&1 &")

    async def command_history_api(request):
        status = True
        message = ""
        command_list = []
        try:
            with sqlite3.connect(os.path.expanduser('~/Library/Application Support/iTerm2/ShellHistory.sqlite')) as db:
                for row in db.execute("select ZCOMMAND from ZCOMMANDHISTORYCOMMANDUSE order  by Z_PK desc limit 100"):
                    if row[0] not in command_list and not row[0].startswith(":") and row[0] != '^C':
                        command_list.append(row[0])
        except Exception as e:
            status = False
            message = f"获取数据错误：{e}"

        return await send_html(json.dumps({
            'status': status,
            'message': message,
            'command_list': command_list[0:50]
        }), request)

    webapp = web.Application()
    webapp.router.add_get('/', main_page)
    webapp.router.add_get('/storage', get_storage_api)
    webapp.router.add_post('/storage', save_storage_api)
    webapp.router.add_delete('/storage', delete_storage_api)
    webapp.router.add_post('/reload_storage', reload_storage_api)
    webapp.router.add_post('/session_storage', save_session_storage_api)
    webapp.router.add_get('/system_storage', get_system_storage_api)
    webapp.router.add_post('/change_store_path', save_store_path_api)
    webapp.router.add_post('/storage_reset_event_send_map', storage_reset_event_send_map_api)
    webapp.router.add_post('/storage_reset_custom_variable_map', storage_reset_custom_variable_map_api)
    webapp.router.add_post('/storage_reset_py_method', storage_reset_py_method_api)
    webapp.router.add_post('/proxy', proxy_api)
    webapp.router.add_get('/command_history', command_history_api)
    webapp.router.add_post('/send_text', send_text_api)
    webapp.router.add_post('/send_hex_code', send_hex_code_api)
    webapp.router.add_post('/exec_shell', exec_shell_api)
    webapp.router.add_get('/selected_text', selected_text_api)
    webapp.router.add_post('/path_file', path_file_api)
    webapp.router.add_post('/iterm2_alert', iterm2_alert_api)
    webapp.router.add_post('/iterm2_confirm', iterm2_confirm_api)
    webapp.router.add_post('/iterm2_prompt', iterm2_prompt_api)
    webapp.router.add_post('/test_event_name', test_event_name_api)
    webapp.router.add_get('/restart', restart_api)
    webapp.router.add_static('/', path=html_home)
    runner = web.AppRunner(webapp)
    await runner.setup()
    site = web.TCPSite(runner, http_web_host, http_web_port)
    await site.start()
