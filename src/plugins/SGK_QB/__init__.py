# -*- coding = utf-8 -*-

import httpx
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command, logger
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg

qb = on_command("QQ号查询", aliases={'QB', 'qb'}, priority=6)


@qb.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("qq", args)  # 如果用户发送了参数则直接赋值


@qb.got("qq", prompt="请输入要查询的qq：\n(输入 'help' 查看帮助)")
async def _(bot: Bot, event: Event, qq=ArgPlainText()):
    if 'help' in qq:
        help_SGK_QB = """
=关于[QQ号查询]功能=
调用机器人方式：
qb + 自己的QQ号
注意：
本功能仅用于学术研究，切勿将其用于违法，伸手必被抓！！！
        """
        await qb.send(help_SGK_QB)
    else:
        try:
            await qb.send("SGK少女祈祷中。。")
            data = await get_data_qb(qq)
            at = MessageSegment.at(str(event.get_user_id))
            if data["status"] == 200:
                ret = MessageSegment.text(data["message"]) + '\n'
                phone = '手机：' + MessageSegment.text(data["phone"]) + '\n'
                phonediqu = MessageSegment.text(data["phonediqu"])
                if isinstance(event, GroupMessageEvent):  # 群里
                    await qb.send(at + ret + phone + phonediqu, reply_message='true')
                if isinstance(event, PrivateMessageEvent):
                    await qb.send(ret + phone + phonediqu, reply_message='true')
                    logger.info(phone)
            if data["status"] == 500:
                await qb.send(at + data['message'], reply_message='true')
        except httpx.ConnectError:
            await qb.send("网络异常，请通知管理员检查服务器网络")


async def get_data_qb(qq: str):
    url_base = "https://zy.xywlapi.cc/qqapi?qq="
    url = url_base + qq
    logger.info(url)
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        r = (await client.get(url)).json()
    return r
