# -*- coding: utf-8 -*-
import iterm2
import json
import typing
from functools import wraps
import aiohttp


def singleton(f):
    instance = {}

    @wraps(f)
    def get_instance(*args, **kwargs):
        if f not in instance:
            instance[f] = f(*args, **kwargs)
        return instance[f]

    return get_instance


async def send_text(app, send_text_context):
    if send_text_context:
        session = app.current_terminal_window.current_tab.current_session
        await session.async_send_text(send_text_context)


async def alert(connection: iterm2.connection.Connection, title='', subtitle='', buttons=None) -> int:
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


async def prompt(connection: iterm2.connection.Connection, title='', subtitle='', placeholder='',
                 default_value='') -> typing.Optional[str]:
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


async def send_http(url, method, headers=None, params=None, data=None, json_data=None):
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
    except Exception as e:
        r['message'] = f"{e}"

    return r


async def send_feishu(token: str, title: str, context: str, note: str = None):
    elements = [{
        'tag': 'markdown',
        'content': context
    }]
    if note:
        elements.append({
            "tag": "note",
            "elements": [{
                "tag": "plain_text",
                "content": note
            }]})
    json_data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "update_multi": True,
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                },
                "template": "blue"
            },
            "elements": elements
        }
    }
    resp = await send_http(url=f'https://open.feishu.cn/open-apis/bot/v2/hook/{token}', method='POST',
                           headers={"Content-Type": "application/json"}, json_data=json_data)
    print(f'飞书：{json.dumps(resp)}')
