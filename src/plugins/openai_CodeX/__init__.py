# -*- coding = utf-8 -*-
import openai
import httpx
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command, logger
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from openaiCofig.apiKeyConfig import api_key

logger.info(api_key)
openai.api_key = api_key



code = on_command('cc', aliases={'CodexC++', 'C++代码'}, priority=10)


@code.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("cc", args)  # 如果用户发送了参数则直接赋值


@code.got('cc', prompt="请问您的代码描述呢？\n(输入 'help' 查看帮助)")
async def _(bot: Bot, event: Event, cc=ArgPlainText('cc')):
    if 'help' in cc:
        await code.finish(_help)
    try:
        await code.send("Coding少女祈祷中...\n(代码发送较慢，请耐心等待，请勿重复发送指令，有问题[zr]联系管理员)")
        code_describe = f"/*C++ {cc}*/"
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=code_describe,
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["；"]
        )
        await code.finish(MessageSegment.text(response["choices"][0]['text']) + '\n' + MessageSegment.at(
            event.get_user_id) + MessageSegment.text("代码生成完毕，请食用~"))
    # except openai.error.APIConnectionError:
    #     await code.send("网络异常，请使用[zr]命令联系管理员检查服务器网络")
    except Exception as e :
        logger.debug(e)
        await code.send("网络异常，请使用[zr]命令联系管理员检查服务器网络")


_help = '''===关于CodeX-C++===
触发条件：
cc + 代码描述
eg：cc 冒泡排序

根据您的描述，使用C++风格生成代码，代码的长度被控制在2048个tokens，请注意您的使用规范'''
