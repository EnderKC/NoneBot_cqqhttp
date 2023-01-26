# -*- coding = utf-8 -*-
import random
from pathlib import Path
import nonebot.adapters.onebot.v11.exception
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_message, on_keyword, logger

bs = on_keyword({'我要白丝', '白丝', 'bs'}, priority=30)
hs = on_keyword({'我要黑丝', '黑丝', 'hs'}, priority=31)


@bs.handle()
async def _(bot: Bot):
    try:
        # 生成随机数
        bs_id = random.randint(1, 182)
        logger.info(bs_id)
        img_path = '白丝 (' + str(bs_id) + ').jpg'
        path = str(Path(__file__).parent / "白丝" / img_path)
        logger.info(path)
        await bs.finish(MessageSegment.image('file:///' + path))
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        await bs.finish("对不起，消息被风控")


@hs.handle()
async def _(bot: Bot):
    try:
        # 生成随机数
        bs_id = random.randint(1, 137)
        logger.info(bs_id)
        img_path = '黑丝 (' + str(bs_id) + ').jpg'
        path = str(Path(__file__).parent / "黑丝" / img_path)
        logger.info(path)
        await hs.finish(MessageSegment.image('file:///' + path))
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        await hs.finish("对不起，消息被风控")
