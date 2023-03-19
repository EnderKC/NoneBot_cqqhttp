# -*- coding = utf-8 -*-
import json
import httpx
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command, logger, on_keyword
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from .httpgai import listpage, onepage
import sqlite3
import random

headers = {"referer": "https://mmzztt.com/",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41"}

meizi = on_keyword({'mz', '妹子图'}, priority=15)


@meizi.handle()
async def _(bot: Bot, event: Event):
    await meizi.send("三次元少女祈祷中....")
    title_id = random.randint(1, 500)
    data = await find_id(title_id)
    title_link = data[0][0]
    imgs = await onepage(title_link)
    logger.info(imgs)
    forward_msgs = await analyze_data(imgs, event.self_id)
    if isinstance(event, GroupMessageEvent):  # 群里
        await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=forward_msgs)
        await meizi.finish("发送完毕", reply_message='true')
    if isinstance(event, PrivateMessageEvent):  # 私人
        await bot.call_api('send_private_forward_msg', user_id=event.user_id, messages=forward_msgs)
        await meizi.finish("发送完毕")


async def createDB():
    new_db = '''
                    create table titles
                    (
                    id integer primary key autoincrement,
                    title text,
                    link text
                    );
                '''  # 创建数据表
    conn = sqlite3.connect('./MeiZi.db')  # 连接数据库
    cursor = conn.cursor()  # 获取游标
    cursor.execute(new_db)  # 执行指令
    conn.commit()  # 提交数据库
    conn.close()  # 关闭数据库
    logger.info("创建数据库完成~")


# title加入数据库
async def add_title(title, link):
    addid = f'''
        INSERT INTO titles (title,link)
        VALUES ('{title}','{link}')
    '''
    conn = sqlite3.connect('./MeiZi.db')
    curses = conn.cursor()
    curses.execute(addid)
    conn.commit()
    conn.close()


# 读取数据库
async def find_id(id):
    getLink = f'''
        SELECT link
        FROM titles
        WHERE id = {id}
    '''
    conn = sqlite3.connect('./MeiZi.db')
    curses = conn.cursor()
    curses.execute(getLink)
    datas = [curses.fetchone()]
    return datas


# 将数据解析，并合成为转发啊形式
async def analyze_data(imgs: list, uin: int) -> list:
    length = len(imgs)
    # 把重要信息合到一条消息
    messages = []
    for i in imgs:
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            b = (await client.get(url=i, headers=headers)).content
        message = MessageSegment.image(b)
        messages.append(message)
    forward_msgs = []
    forward_msg = {
        'type': 'node',
        'data': {
            'name': '情报员',
            'uin': uin,
            'content': f"请注意身体哦~"
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
