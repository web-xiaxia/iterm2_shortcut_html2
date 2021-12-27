# -*- coding: utf-8 -*-
import re
from aiohttp.connector import Connection

import sqlite3
from iterm2.app import App
from storage import Storage
from typing import Tuple, List

import iterm2
import json
import os
import aiohttp
from aiohttp import web
import subprocess

CONTEXT_INCLUDE_PATTERN = re.compile(r'''(<context-include src=["|'](.*?)["|']/>)''')
HTML_INCLUDE_PATTERN = re.compile(r'''(<html-include src=["|'](.*?)["|']/>)''')
BLOCK_STYLE_PATTERN = re.compile(r'''\{% block style %\}(.*?)\{% endblock %\}''', re.DOTALL)
BLOCK_SCRIPT_PATTERN = re.compile(r'''\{% block script %\}(.*?)\{% endblock %\}''', re.DOTALL)
BLOCK_CONTEXT_PATTERN = re.compile(r'''\{% block context %\}(.*?)\{% endblock %\}''', re.DOTALL)


async def api_register(connection: Connection, app: App, STORAGE_DATA: Storage, main_file: str, main_home: str,
                       html_home: str):
    async def my_send_text(send_text=''):
        session = app.current_terminal_window.current_tab.current_session
        await session.async_send_text(send_text.replace('|==f==h==|', '"'))

    def include_block(html: str) -> Tuple[List[str], List[str], List[str]]:
        style_block = BLOCK_STYLE_PATTERN.findall(html)
        script_block = BLOCK_SCRIPT_PATTERN.findall(html)
        context_block = BLOCK_CONTEXT_PATTERN.findall(html)

        return style_block, script_block, context_block

    def include_html_util(html_text: str) -> str:
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
                    style_block, script_block, context_block = include_block(fp.read())
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
            return await send_html(include_html_util(html_text), request, content_type='text/html')

    async def get_storage_api(request):
        try:
            return await send_html(json.dumps(await STORAGE_DATA.get_storage(), sort_keys=True, indent=4), request)
        except Exception:
            return await send_html("{}", request)

    async def save_storage_api(request):
        data = await request.json()
        storage_data_version_id = data.get('storage_data_version_id')
        new_storage = data.get('storage')
        bak = data.get('bak')
        if bak:
            print(f"{new_storage.get('storage_data_version_id')} , {storage_data_version_id}")

        storage = await STORAGE_DATA.get_storage()
        if storage_data_version_id != storage.get('storage_data_version_id'):
            return await send_error(request, "保存失败，请刷新或重新打开页面")

        await STORAGE_DATA.set_storage(new_storage, bak=bak)
        return await send_ok(request)

    async def delete_storage_api(request):
        await STORAGE_DATA.delete_storage()
        return await send_ok(request)

    async def storage_reset_event_send_map_api(request):
        await STORAGE_DATA.reset_event_send_map()
        return await send_ok(request)

    async def storage_reset_custom_variable_map_api(request):
        await STORAGE_DATA.reset_custom_variable_map()
        return await send_ok(request)

    async def storage_reset_py_method_api(request):
        await STORAGE_DATA.reset_xpy_method()
        return await send_ok(request)

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def proxy_api(request):
        request_data = await request.json()
        url = request_data.get('url')
        method = request_data.get('method')
        headers = request_data.get('headers')
        params = request_data.get('params', None)
        data = request_data.get('data', None)
        json_data = request_data.get('json_data', None)
        r = {
            "status": False,
            "data": None,
            "message": ""
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method.upper(), url, params=params, data=data, json=json_data,
                                           headers=headers,
                                           verify_ssl=False) as resp:
                    response_headers = {}
                    for key, v in resp.headers.items():
                        response_headers[key] = v
                    resp_text = await resp.text()
                    r['data'] = {
                        'status': f'{resp.status}',
                        'text': f'{resp_text}',
                        'headers': response_headers
                    }
                    r.datta = resp.text()
        except Exception as e:
            r['message'] = f"{e}"

        return await send_html(json.dumps(r), request)

    async def send_text_api(request):
        data = await request.post()
        send_text = data['send_text']
        await my_send_text(send_text)
        return await send_ok(request)

    async def send_hex_code_api(request):
        data = await request.post()
        session = app.current_terminal_window.current_tab.current_session
        await session.async_inject(bytes(str(data['send_hex_code']), encoding="utf-8"))
        return await send_ok(request)

    def exec_shell(shell_text: str) -> Tuple[bool, List[str]]:
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

    async def exec_shell_api(request):
        data = await request.post()
        shell_text = data['shell']
        status, result = exec_shell(shell_text)

        return await send_html(json.dumps({
            'status': status,
            'result': result,
        }), request)

    async def selected_text_api(request):
        session = app.current_terminal_window.current_tab.current_session
        selection = await session.async_get_selection()
        selected_text = await session.async_get_selection_text(selection)
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

    async def item2_alert(title='', subtitle=''):
        alert = iterm2.Alert(title, subtitle)
        await alert.async_run(connection)

    async def iterm2_alert_api(request):
        data = await request.post()
        title = data['title']
        subtitle = data['subtitle']
        await item2_alert(title, subtitle)
        return await send_ok(request)

    async def iterm2_confirm_api(request):
        data = await request.json()
        title = data['title']
        subtitle = data['subtitle']
        buttons = data['buttons']
        alert = iterm2.Alert(title, subtitle)
        for button in buttons:
            alert.add_button(button)
        return await send_html(json.dumps({
            'status': await alert.async_run(connection)
        }), request)

    async def iterm2_prompt_api(request):
        data = await request.json()
        title = data['title']
        subtitle = data['subtitle']
        default_value = data['default_value']
        alert = iterm2.TextInputAlert(title, subtitle, '', default_value)
        return await send_html(json.dumps({
            'status': await alert.async_run(connection)
        }), request)

    async def restart_api(request):
        # await site.stop()
        # await runner.shutdown()
        os.system("ps -ef | grep python | grep -v grep | grep shortcut_html2.py | awk '{print $2}' | xargs kill -9  "
                  "&& nohup /bin/bash /Applications/iTerm.app/Contents/Resources/it2_api_wrapper.sh "
                  + main_home + "/../iterm2env/versions/3.7.9/bin/python3 "
                  + main_home + "/shortcut_html2.py 2>&1 &")

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
    webapp.router.add_get('/restart', restart_api)
    webapp.router.add_static('/', path=html_home)
    runner = web.AppRunner(webapp)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 9998)
    await site.start()

    # Register a custom toolbelt tool that shows the web pages served by the server in this script.
    await iterm2.tool.async_register_web_view_tool(connection, "Targeted Input2", "com.iterm2.example.targeted-input2",
                                                   False, "http://localhost:9998/")
