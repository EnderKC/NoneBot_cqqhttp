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
from .getdata import df_data

setu = on_command('setu', aliases={'涩图', 'st'}, priority=10)

xjj = on_keyword({'xjj', '来个小姐姐'}, priority=11)

df = on_keyword({'df', '来个东方'}, priority=12)


@setu.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("tag", args)  # 如果用户发送了参数则直接赋值


@setu.got('tag', prompt="请问您的tag呢？\n(输入 'help' 查看帮助)")
async def _(bot: Bot, event: Event, tags=ArgPlainText('tag')):
    if isinstance(event, GroupMessageEvent):  # 如果时群聊
        if 'help' in tags:
            await setu.finish(MessageSegment.at(event.user_id) + '\n' + _help)
        tag_json = {
            'r18': 0,  # 不包含r18
            'num': 1,  # 数量1
            'tag': [tags],  # 使用tags
            'size': ['regular', 'original'],  # 大小为regular
            'excludeAI': 1,  # 排除AI作品
        }
        try:
            data = await get_data(tag_json)
            await setu.send("涩涩少女祈祷中....")
            logger.info(data['urls'])
            logger.info(data['tags'])
            await setu.send(
                MessageSegment.image(data['urls']['regular']) + '\n' + "标题：" +
                MessageSegment.text(data['title']) + '\n' + "作品pid: " +
                MessageSegment.text(data['pid']) + '\n' + '作者：' +
                MessageSegment.text(data['author']) + '\n' +
                MessageSegment.at(event.user_id)
            )
        except nonebot.adapters.onebot.v11.exception.NetworkError:
            await setu.send("发送超时（原因可能是图片体积太大，稍等一会可能会发送成功）")
        except httpx.ConnectError:
            await setu.send("网络异常，请通知管理员检查服务器网络")
        except Exception as e:
            logger.error(f'机器人被风控了{e}')
            await setu.send('消息可能被风控，请稍后再试，或者私聊机器人')
    if isinstance(event, PrivateMessageEvent):  # 如果私聊
        if 'help' in tags:
            await setu.finish(MessageSegment.at(event.user_id) + '\n' + _help)
        tag_json = {
            'r18': 2,  # 混合r18
            'num': 1,  # 数量1
            'tag': tags,  # 使用tags
            'size': ['regular', 'original'],  # 大小为regular
            'excludeAI': 1,  # 排除AI作品
        }
        try:
            data = await get_data(tag_json)
            await setu.send("涩涩少女祈祷中....")
            logger.info(data['urls'])
            logger.info(data['tags'])
            await setu.send(
                MessageSegment.image(data['urls']['regular']) + '\n' + "标题：" +
                MessageSegment.text(data['title']) + '\n' + "作品pid: " +
                MessageSegment.text(data['pid']) + '\n' + '作者：' +
                MessageSegment.text(data['author'])
            )
        except nonebot.adapters.onebot.v11.exception.NetworkError:
            await setu.send("发送超时（原因可能是图片体积太大，稍等一会可能会发送成功）")
        except httpx.ConnectError:
            await setu.send("网络异常，请通知管理员检查服务器网络")
        except Exception as e:
            logger.error(f'机器人被风控了{e}')
            await setu.send('消息可能被风控，请稍后再试，或者私聊机器人')


async def get_data(tag_json: dict):
    logger.info(json)
    url = 'https://api.lolicon.app/setu/v2'
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        r = (await client.post(url, json=tag_json)).json()
    return r['data'][0]


@xjj.handle()
async def _(bot: Bot, event: Event):
    try:
        await xjj.send(MessageSegment.image('https://img.moehu.org/pic.php?id=xjj'))
        await xjj.finish("请注意身体", reply_message='true')
    except httpx.ConnectError:
        await setu.send("网络异常，请通知管理员检查服务器网络")


@df.handle()
async def _(bot: Bot, event: Event):
    img = await df_data()
    await df.send(MessageSegment.image(img))
    await xjj.finish("东方来咯~", reply_message='true')


_help = '''=关于[setu]功能的概述=
调用机器人方式：
setu/涩图+tag
eg:setu 黑丝
(群聊默认不带R18，私聊随机R18)
请您注意身体健康~'''
