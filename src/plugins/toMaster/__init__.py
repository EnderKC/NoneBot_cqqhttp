# -*- coding = utf-8 -*-

import nonebot
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent, MessageEvent
from nonebot import on_command, logger
from nonebot.adapters import Message, Bot, Event
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from .config import Config


plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())
if plugin_config.master_id:
    QQ_master = plugin_config.master_id


master = on_command('主人', aliases={'zr', 'master'}, priority=10)


@master.handle()
async def _(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg('msg', args)  # 如果用户发送了参数则直接赋值


@master.got('msg', prompt="请问您要对主人说什么呢？\n(输入 'help' 查看帮助)")
async def _(bot: Bot, event: MessageEvent, msg=ArgPlainText('msg')):
    if 'help' in msg:
        await master.finish(_help)
    reply_msg = '已经向主人发送~'
    await bot.send(event, message=reply_msg, reply_message='true')
    if isinstance(event, PrivateMessageEvent):
        msg_p = f'''来自私聊QQ：{event.user_id}
昵称：{event.sender.nickname}

消息：{msg}
id：{event.message_id}'''
        await bot.call_api('send_private_msg', message=msg_p, user_id=QQ_master)
        master.stop_propagation()  # 阻断事件传播
    if isinstance(event, GroupMessageEvent):
        msg_p = f'''来自群聊：{event.group_id}
QQ:{event.user_id}
昵称：{event.sender.nickname}

消息：{msg}
id：{event.message_id}'''
        await bot.call_api('send_private_msg', message=msg_p, user_id=QQ_master)
        master.stop_propagation()  # 阻断事件传播


_help = '''==向开发者反应==
zr/主人 + 消息
(提交BUG，交流感情,bot建议)
可以直接把消息发送给开发者，方便他在摸鱼时间也能专心工作~'''
