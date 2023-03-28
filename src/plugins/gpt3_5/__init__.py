# -*- coding = utf-8 -*-
import openai
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command, logger, on_message
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from openaiCofig.apiKeyConfig import api_key

logger.info(api_key)
openai.api_key = api_key

# 添加block参数来指定该事件响应器是否会在执行完成后进行阻断
gpt = on_message(priority=50, rule=to_me(), block=True)


@gpt.handle()
async def _(matcher: Matcher, event: Event):
    logger.info(event.get_plaintext())
    result = ask_gpt(event.get_plaintext())
    logger.info(result)
    if (len(event.get_plaintext()) > 200):
        await gpt.send("您发送的消息太长了")
    await gpt.finish(result)


def ask_gpt(prompt):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "一个有礼貌 可爱的 猫娘"},
            {"role": "user", "content": prompt}
        ]
    )

    message = completions["choices"][0]["message"]['content']
    return message
