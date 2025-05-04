# -*- coding: utf-8 -*-
from api.exec_api import ExecApi
from api.py_api import PyApi

import sqlite3
from common import utils
from common.session_storage_data import SessionStorageData

import json
import os

from aiohttp import web

from common.storage_data import StorageHelper


async def register(session_storage_data: SessionStorageData, storage_data: StorageHelper, py_api: PyApi, exec_api: ExecApi, main_home: str, html_home: str, http_web_host: str, http_web_port: int):
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

    async def get_storage_api(request):
        return await send_html(await storage_data.read(), request)

    async def save_storage_api(request):
        data = await request.json()
        await storage_data.save(json.dumps(data))
        return await send_ok(request)

    async def save_session_storage_api(request):
        data = await request.json()
        key = data.get('key')
        value = data.get('value')
        await session_storage_data.set_storage(key, value)
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
        data = await request.json()
        send_text_context = data['send_text']
        run_type = data['run_type'] if 'run_type' in data else ''
        await py_api.send_text(send_text_context, run_type)
        return await send_ok(request)

    async def send_hex_code_api(request):
        data = await request.json()
        await py_api.send_hex_code(data['send_hex_code'])
        return await send_ok(request)

    async def exec_shell_api(request):
        data = await request.json()
        shell_text = data['shell']
        status, result = await py_api.exec_shell(shell_text)

        return await send_html(json.dumps({
            'status': status,
            'result': result,
        }), request)

    async def exec_py_api(request):
        data = await request.json()
        py_text = data['py']
        agrs = data['agrs']
        result = await exec_api.code_exec(py_text, agrs)
        return await send_html(json.dumps({
            'status': True,
            'result': result,
        }), request)

    async def selected_text_api(request):
        selected_text = await py_api.selected_text()
        return await send_html(json.dumps({
            'selected_text': selected_text,
        }), request)

    async def path_file_api(request):
        data = await request.json()
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
        data = await request.json()
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

    async def register_trigger_api(request):
        data = await request.json()
        trigger_name = data['name']
        await py_api.register_trigger(trigger_name)
        return await send_ok(request)

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
    webapp.router.add_get('/api/storage', get_storage_api)
    webapp.router.add_post('/api/storage', save_storage_api)
    webapp.router.add_post('/api/session_storage', save_session_storage_api)
    webapp.router.add_post('/api/proxy', proxy_api)
    webapp.router.add_get('/api/command_history', command_history_api)
    webapp.router.add_post('/api/send_text', send_text_api)
    webapp.router.add_post('/api/send_hex_code', send_hex_code_api)
    webapp.router.add_post('/api/exec_shell', exec_shell_api)
    webapp.router.add_post('/api/exec_py', exec_py_api)
    webapp.router.add_get('/api/selected_text', selected_text_api)
    webapp.router.add_post('/api/path_file', path_file_api)
    webapp.router.add_post('/api/iterm2_alert', iterm2_alert_api)
    webapp.router.add_post('/api/iterm2_confirm', iterm2_confirm_api)
    webapp.router.add_post('/api/iterm2_prompt', iterm2_prompt_api)
    webapp.router.add_post('/api/register_trigger', register_trigger_api)
    webapp.router.add_post('/api/test_event_name', test_event_name_api)
    webapp.router.add_static('/', path=html_home)
    runner = web.AppRunner(webapp)
    await runner.setup()
    site = web.TCPSite(runner, http_web_host, http_web_port)
    await site.start()
