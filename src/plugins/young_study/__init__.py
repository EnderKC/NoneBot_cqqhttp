# -*- coding = utf-8 -*-
from nonebot.drivers.websockets import logger
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
import httpx
from nonebot.adapters.onebot.v11 import Event

# 定义一个事件响应器
study = on_keyword({"青年大学习", "大学习", '学大习', 'qndxx'}, priority=49)


@study.handle()
async def study_fun(event: Event):
    url = "https://api.xbyzs.cf/dxx"
    try:
        await study.send("大学习少女祈祷中....")
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            r = (await client.get(url=url))
            status = r.status_code
        logger.info(status)
        if status == 307:
            img = r.headers['location']
            logger.info(r.headers)
            await study.send(MessageSegment.image(img))
            await study.finish(MessageSegment.at(event.get_user_id)+'青年大学习截图已发送，请注意查收~', reply_message='true')
    except httpx.ConnectError:
        await study.finish("服务器网络出错，请输入指令[zr]联系管理员检查服务器网络。", reply_message='true')
