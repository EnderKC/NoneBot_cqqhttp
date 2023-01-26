# -*- coding = utf-8 -*-
import random
from datetime import date

from nonebot.adapters.onebot.v11 import Message
from nonebot.plugin import on_keyword
# 获取命令型消息命令前缀
from nonebot.params import Keyword

Repeat = on_keyword({"复读", '复读机', 'fd'}, priority=49)


@Repeat.handle()
async def Repeat_handle(event, kw: str = Keyword()):
    info = event.get_message()
    info = str(info).replace(f'{kw}', '')
    # 解析数据信息
    await Repeat.finish(
        Message(f'[CQ:at,qq={event.get_user_id()}]复读：{info}')
    )
