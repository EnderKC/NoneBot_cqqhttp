# -*- coding = utf-8 -*-
import asyncio
import ssl

import httpx
import re
from nonebot import on_command, logger
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot.internal.adapter import event
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Arg, ArgPlainText
from nonebot.params import CommandArg
from .Data import get_date, analyze_data

magnetic = on_command("资源", aliases={'搜索', '磁力搜索', 'cl'}, priority=5)


@magnetic.handle()
async def handle_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("search", args)  # 如果用户发送了参数则直接赋值


@magnetic.got("search", prompt="你想查询什么呢？\n(输入 'help' 查看帮助)")
async def handle_magnetic(bot: Bot, event: Event, search=Arg(), search_con=ArgPlainText('search')):
    global data  # 设置为全局变量
    try:
        page = re.findall(r'\s(\d)', search_con)[0]
        search_con = search_con.replace(page, '')
    except IndexError:
        page = "1"
    logger.info(f"page:{page}")
    logger.info(f"con :{search_con}")
    if 'help' in search_con:  # 后期改进为正则匹配
        at = MessageSegment.at(event.get_user_id())
        help_ = MessageSegment.text('''
=关于[资源]功能的概述=
调用机器人方式：
资源 (要搜索的内容) (页面)
如果页面不填默认为第一页
''')
        await magnetic.send(at + help_)
    else:
        try:
            await magnetic.send("磁力少女祈祷中....")
            if page:
                data = await Data.get_date(search_con, page)
            forward_msgs = await Data.analyze_data(data, event.self_id, page)
            if isinstance(event, GroupMessageEvent):  # 群里
                await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=forward_msgs)
            if isinstance(event, PrivateMessageEvent):  # 私人
                await bot.call_api('send_private_forward_msg', user_id=event.user_id, messages=forward_msgs)
        except httpx.ConnectError:
            await magnetic.send("网络异常，请通知管理员检查服务器网络")
        except ssl.SSLWantReadError:
            await magnetic.send("网络请求超时，请稍后再试\n（API质量不好）")
