# -*- coding = utf-8 -*-
import httpx


async def df_data():
    url = 'https://img.paulzzh.com/touhou/random'
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        r = (await client.get(url)).headers
    return r['Location']
