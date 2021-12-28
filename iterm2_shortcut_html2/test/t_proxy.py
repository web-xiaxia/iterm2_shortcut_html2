# -*- coding: utf-8 -*-

import asyncio
import json
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', 'https://www.baidu.com', verify_ssl=False, headers={
            'xxx': "xxxx"
        }) as resp:
            b = await resp.text()
            data = {}
            for key, v in resp.headers.items():
                data[key] = v

            print(b)
            print(json.dumps(data))


asyncio.run(main(), debug=True)
