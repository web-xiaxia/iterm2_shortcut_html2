# -*- coding: utf-8 -*-
import hashlib
import json
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


async def md5(text: str) -> str:
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


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
