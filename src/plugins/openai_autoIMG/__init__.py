# -*- coding = utf-8 -*-
import os
import openai
import httpx
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command, logger
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg

oi = on_command('oi', aliases={'autoimg', '生成图片'}, priority=10)

openai.api_key = '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'


@oi.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("img_describe", args)  # 如果用户发送了参数则直接赋值


@oi.got('img_describe', prompt="请问您的图片描述呢？\n(输入 'help' 查看帮助)")
async def _(bot: Bot, event: Event, describe=ArgPlainText('img_describe')):
    if 'help' in describe:
        await oi.finish(_help)
    # 如果不是help
    try:
        await oi.send("ai少女祈祷中...\n(图片发送较慢，请耐心等待，请勿重复发送指令，有问题[zr]联系管理员)")
        response = openai.Image.create(
            prompt=describe,
            n=1,
            size='512x512',
        )
        msg = MessageSegment.image(response['data'][0]['url']) + '\n' + MessageSegment.text(
            "图片生成完毕") + MessageSegment.at(event.get_user_id())
        await oi.finish(msg)
    except openai.error.APIConnectionError:
        await oi.send("网络异常，请使用[zr]命令联系管理员检查服务器网络")
    except openai.error.InvalidRequestError:
        await oi.send("对不起，我们目前不支持生成包括色情、血腥、仇恨、极端画面，请您替换您的描述" + MessageSegment.at(event.get_user_id()))


_help = '''===关于AutoImg===
指令输入方式：

oi/生成图片 + 图片描述信息
eg：oi 一只白色小猫

警告：图片默认为 512*512 正方形画质，生成AI来自openai，每生成一张图片，开发者要向openai支付不等的费用，请适当游玩。'''
