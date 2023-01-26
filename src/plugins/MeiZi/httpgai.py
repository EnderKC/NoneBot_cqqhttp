# # Created by 孤独的我 at 2022/6/18 23:25:07
import asyncio
from nonebot import on_command, logger, on_keyword
from bs4 import BeautifulSoup
from lxml import etree
import httpx
from typing import List
import binascii
import json
import re
from crypto.Cipher import AES
from crypto.Hash import MD5

headers = {"referer": "https://mmzztt.com/",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41",
           "Content-Type": "text/html"}


# 抓列表页
async def listpage(page):
    url = 'https://mmzztt.com/photo/page/' + str(page) + '/'
    dict = {}
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        raw = (await client.get(url, headers=headers)).text
    soup = BeautifulSoup(raw, 'lxml')
    for i in range(7, 31):
        dict[soup.find_all('li')[i].find('div').find_all('div')[2].find('h2').text] = \
            soup.find_all('li')[i].find('div').find_all('div')[2].find('a')['href']
    return dict


# 抓详情页
async def onepage(url):
    imgs = []
    pid = int(url.split('/')[-1])
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        raw = (await client.get(url, headers=headers)).text
    html = etree.HTML(raw)
    cache_sign = html.xpath("//body/comment()")[0].__str__()[68:-3]
    IV = "".join([str(pid % i % 9) for i in range(2, 18)]).encode()
    key = (
        MD5.new(f"{pid}6af0ce23e2f85cd971f58bdf61ed93a6".encode())
        .hexdigest()[8:24]
        .encode()
    )
    aes = AES.new(key, AES.MODE_CBC, IV)
    result = aes.decrypt(binascii.a2b_hex(cache_sign)).rstrip()
    result = re.findall(r"(\[.*\])", result.decode())[0]
    des = json.loads(result)
    url = html.xpath("/html/body/section[1]/div/div/main/article/figure/img")[0].attrib['src'].replace(
        html.xpath("/html/body/section[1]/div/div/main/article/figure/img")[0].attrib['src'].split('/')[-1], '')
    for i in des:
        imgs.append(url + i)
    return imgs
