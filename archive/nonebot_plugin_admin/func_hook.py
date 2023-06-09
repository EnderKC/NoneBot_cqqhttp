# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 17:52
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : func_hook.py
# @Software: PyCharm
from nonebot import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    ActionFailed,
    GroupMessageEvent,
    GroupRequestEvent,
    Event,
)
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, IgnoredException
from nonebot.typing import T_State
from pathlib import Path

from .config import plugin_config, global_config
from .path import *
from .utils import check_func_status

cb_notice = plugin_config.callback_notice
su = global_config.superusers
parent_path = str(Path(__file__).parent).split("/")[-1]

@run_preprocessor
async def _(matcher: Matcher, bot: Bot, state: T_State, event: Event):
    module = str(matcher.module_name).split('.')
    if len(module) < 2 or module[-2] != parent_path: return  # 位置与文件路径有关
    which_module = module[-1]
    # logger.info(f"{which_module}插件开始hook处理")
    if isinstance(event, GroupMessageEvent):
        gid = event.group_id
        try:
            if which_module in admin_funcs:
                status = await check_func_status(which_module, str(gid))
                if not status and which_module not in ['auto_ban', 'img_check']:  # 违禁词检测和图片检测日志太多了，不用logger记录或者发消息记录
                    if cb_notice:
                        await bot.send_group_msg(group_id=gid,
                                                 message=f"功能处于关闭状态，发送【开关{admin_funcs[which_module][0]}】开启")
                    raise IgnoredException('未开启此功能...')
                elif not status and which_module in ['auto_ban', 'img_check']:
                    raise IgnoredException('未开启此功能...')
        except ActionFailed:
            pass
        except FileNotFoundError:
            pass
    elif isinstance(event, GroupRequestEvent):
        gid = event.group_id
        try:
            if which_module == 'requests':
                logger.info(event.flag)
                if event.sub_type == 'add':
                    status = await check_func_status(which_module, str(gid))
                    if not status:
                        re_msg = f"群{gid}收到{event.user_id}的加群请求，flag为：{event.flag}，但审批处于关闭状态\n发送【请求同意/拒绝 " \
                                 f"flag】来处理次请求，例：\n请求同意{event.flag}\n发送【开关{admin_funcs[which_module][0]}】开启，或人工审批 "
                        logger.info(re_msg)
                        if cb_notice:
                            try:
                                for qq in su:
                                    await bot.send_msg(user_id=qq, message=re_msg)
                            except ActionFailed:
                                logger.info('发送消息失败,可能superuser之一不是好友')
                        raise IgnoredException('未开启此功能...')
                else:
                    pass
        except ActionFailed:
            pass
        except FileNotFoundError:
            pass
