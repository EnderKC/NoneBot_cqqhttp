# -*- coding = utf-8 -*-
import nonebot
from nonebot import on_request, logger
# from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Event, Bot, FriendRequestEvent, GroupRequestEvent
from .config import Config


plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())
if plugin_config.accept_invite:
    accept_id = plugin_config.accept_invite


invite_group = on_request(priority=1)


@invite_group.handle()
async def first_receive(bot: Bot, event: Event):
    if event.get_event_name() in {'request.group.invite', 'request.friend'}:
        logger.info(event.get_event_name())
        if event.get_event_name() == 'request.group.invite':
            if event.get_user_id() not in accept_id:
                logger.info("拒绝")
                logger.info(event.get_user_id)
                logger.info(type(event.get_user_id()))
                await event.reject(bot)
                return
            else:
                logger.info("同意")
                await event.approve(bot)
                return
        elif event.get_event_name() == 'request.friend':
            logger.info("同意")
            await event.approve(bot)
            return
        else:
            logger.info("未知错误")



