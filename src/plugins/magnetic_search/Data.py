# -*- coding = utf-8 -*-
import httpx
from nonebot import on_command, logger
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot
from nonebot.internal.adapter import event
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Arg, ArgPlainText
from nonebot.params import CommandArg


# 获取json格式的查询数据
async def get_date(search_con: str, page: str = '1'):
    url_base = "https://api.jucili.com/api.php?s=nyaa"
    search_con = '&q=' + search_con
    page = '&p=' + page
    url = url_base + search_con + page
    logger.info(url)
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        r = (await client.get(url=url)).json()
    logger.info("132")
    return r['data']


'''
 [{
    "type": "node",
    "data": {
        "name": "使用迅雷等bit软件下载",
        "uin": uin,
        "content": Message(await i.to_string())
        }
    }]
'''


# 将数据解析，并合成为转发啊形式
async def analyze_data(data: list[dict], uin: int, page:int = 1) -> list:
    length = len(data)
    # 把重要信息合到一条消息
    messages = []
    for i in data:
        message = i["title"] + '\n' + i["time"] + '\n' + i["size"] + '\n' + i["magnet"]
        messages.append(message)
    forward_msgs = []
    forward_msg = {
        'type': 'node',
        'data': {
            'name': '情报员',
            'uin': uin,
            'content': f"当前第{page}页"
        }
    }
    forward_msgs.append(forward_msg)
    for i in messages:
        forward_msg = {
            'type': 'node',
            'data': {
                'name': '情报员',
                'uin': uin,
                'content': i
            }
        }
        forward_msgs.append(forward_msg)
    return forward_msgs
