# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/24 17:33
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : switcher.py
# @Software: PyCharm
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment, ActionFailed
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from pyppeteer import launch

from .path import *
from .utils import load, upload, fi, log_fi

switcher = on_command('开关', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@switcher.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent, state: T_State):
    gid = str(event.group_id)
    user_input_func_name = str(state['_prefix']['command_arg'])
    for func in admin_funcs:
        if user_input_func_name in admin_funcs[func]:
            funcs_status = (await load(switcher_path))
            if funcs_status[gid][func]:
                funcs_status[gid][func] = False
                await upload(switcher_path, funcs_status)
                await fi(matcher, '已关闭' + user_input_func_name)
            else:
                funcs_status[gid][func] = True
                await upload(switcher_path, funcs_status)
                await fi(matcher, '已开启' + user_input_func_name)


switcher_html = on_command('开关状态', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@switcher_html.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    gid = str(event.group_id)
    funcs_status = (await load(switcher_path))
    try:
        from os.path import dirname
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(str(dirname(__file__))))
        template = env.get_template('switcher.html')
        html = template.render(funcs_status=funcs_status[gid], funcs_name=admin_funcs, gid=gid)
        with open((template_path / f"{gid}.html").resolve(), 'w', encoding='utf-8') as f:
            f.write(html)
            f.close()
        await save_image(f"file:///{(template_path / f'{gid}.html').resolve()}",
                         img_path=(re_img_path / f"{gid}.png").resolve())
        with open((re_img_path / f"{gid}.png").resolve(), 'rb') as f:
            img_bytes = f.read()
        await fi(matcher, MessageSegment.image(img_bytes))
    except ActionFailed:
        await log_fi(matcher,
                     '当前群组开关状态：\n' + '\n'.join(
                         [f"{admin_funcs[func][0]}：{'开启' if funcs_status[gid][func] else '关闭'}" for func in
                          admin_funcs]),
                     '可能被风控，已使用文字发送', err=True)
    except FinishedException:
        pass
    except Exception as e:
        await log_fi(matcher,
                     '当前群组开关状态：\n' + '\n'.join(
                         [f"{admin_funcs[func][0]}：{'开启' if funcs_status[gid][func] else '关闭'}" for func in
                          admin_funcs]),
                     f'开关渲染网页并截图失败，已使用文字发送，错误信息：\n{"-" * 30}{type(e)}: {e}{"-" * 30}', err=True)


async def save_image(url, img_path):
    """
    导出图片
    :param url: 在线网页的url
    :param img_path: 图片存放位置
    :return:
    """
    browser = await launch(options={'args': ['--no-sandbox']}, handleSIGINT=False)
    page = await browser.newPage()
    # 加载指定的网页url
    await page.goto(url)
    # 设置网页显示尺寸
    await page.setViewport({'width': 1920, 'height': 1080})
    """
    path: 图片存放位置
    clip: 位置与图片尺寸信息
        x: 网页截图的x坐标
        y: 网页截图的y坐标
        width: 图片宽度
        height: 图片高度
    """
    await page.screenshot({'path': img_path, 'clip': {'x': 0, 'y': 0, 'width': 320, 'height': 500}})
    await browser.close()
