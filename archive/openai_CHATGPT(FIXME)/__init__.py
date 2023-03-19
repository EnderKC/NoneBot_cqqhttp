# -*- coding = utf-8 -*-
import json
import sqlite3
from typing import List, Any
import io

import httpx
from nonebot_plugin_htmlrender import (
    text_to_pic,
    md_to_pic,
    template_to_pic,
    get_new_page,
)
from pathlib import Path
from nonebot.adapters.onebot.v11 import unescape
from revChatGPT.ChatGPT import Chatbot
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command, logger
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg

config = {
    "email": "1272591828@qq.com",
    "password": "20021001+.",
    "isMicrosoftLogin": True
    # "proxy": "http//:1270.0.1:7890"
}

cp = on_command('cp', priority=20)
dbpath = 'src/plugins/openai_CHATGPT(FIXME)/ConversationQQ.db'
csspath = 'src/plugins/openai_CHATGPT(FIXME)/templates/markdown.css'
master_id = '180407175'


@cp.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    await cp.finish("您好，非常抱歉，由于ChatGPT添加Cloudflare的反机器人保护，本插件将无限期挺管用，敬请期待！。")
    '''
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("text", args)  # 如果用户发送了参数则直接赋值


@cp.got('text', prompt="请问您要发送的信息呢？\n(输入 'help' 查看帮助)")
async def _(bot: Bot, event: Event, text=ArgPlainText('text')):
    if 'help' in text:
        await cp.finish(_help)
    if text == '新建数据库' and event.get_user_id == master_id:
        await NewDatabase()
        await cp.finish("管理员您好，我们已经创建数据库！")
    try:
        if isinstance(event, PrivateMessageEvent):
            if text == '新建会话':
                await new_converQ(event.user_id)
                await cp.finish("已新建会话~")
            await cp.send("我们已经将您的消息发送给OpenAI，请耐心等待回复，有问题[zr]联系管理员")
            qid = event.user_id
            chatbot = Chatbot(config, conversation_id=None)
            chatbot.refresh_session()  # 新建会话
            datas = await get_cidQ(qid)
            logger.info(len(datas))
            logger.info(datas)
            if not datas[0]:
                logger.info("进if")
                msg = chatbot.get_chat_response(text)  # 向Chatgpt获取数据
                msg_pic = await md_to_pic(msg['message'],
                                          css_path=str(Path(__file__).parent / "templates" / "markdown.css"),
                                          width=800)
                logger.info(msg)
                cid = msg['conversation_id']  # 获取会话id
                pid = msg['parent_id']
                await add_cidQ(qid, cid, pid)
                await cp.send("您好，数据库中没有您之前的记录，已经为您创建新的对话~")
                await bot.send(event, message=MessageSegment.image(msg_pic))  # 给用户发送消息
            else:
                # 如果数据库内有记录
                cid = str(datas[0][3])
                pid = str(datas[0][4])
                logger.info("cid" + datas[0][3])
                logger.info("pid" + datas[0][4])
                chatbot.conversation_id = cid
                chatbot.parent_id = pid
                msg = await chatbot.get_chat_response(text)
                msg_pic = await md_to_pic(msg['message'],
                                          css_path=str(Path(__file__).parent / "templates" / "markdown.css"),
                                          width=800)
                await update_pidQ(qid, msg['conversation_id'], msg['parent_id'])
                await cp.finish(MessageSegment.image(msg_pic))  # 给用户发送消息
        if isinstance(event, GroupMessageEvent):
            if text == '新建会话':
                await new_converG(event.group_id)
                await cp.finish("已新建会话~")
            logger.info("群聊")
            await bot.send(event, message="GPT少女祈祷中...\n有问题[zr]联系管理员", reply_message='true')
            gid = event.group_id
            chatbot = Chatbot(config, conversation_id=None)
            chatbot.refresh_session()  # 新建会话
            datas = await get_cidG(gid)
            logger.info(len(datas))
            logger.info(datas)
            if len(datas) == 0:
                logger.info("进if")
                msg = await chatbot.get_chat_response(text)  # 向Chatgpt获取数据
                msg_pic = await md_to_pic(msg['message'],
                                          css_path=str(Path(__file__).parent / "templates" / "markdown.css"),
                                          width=800)
                logger.info(msg)
                cid = msg['conversation_id']  # 获取会话id
                pid = msg['parent_id']
                await add_cidG(gid, cid, pid)
                await cp.send("您好，数据库中没有您之前的记录，已经为您创建新的对话~")
                await cp.send(MessageSegment.image(msg_pic))  # 给用户发送消息
            else:
                # 如果数据库内有记录
                cid = str(datas[0][3])
                pid = str(datas[0][4])
                logger.info("cid" + datas[0][3])
                logger.info("pid" + datas[0][4])
                chatbot.conversation_id = cid
                chatbot.parent_id = pid
                msg = await chatbot.get_chat_response(text)
                msg_pic = await md_to_pic(msg['message'],
                                          css_path=str(Path(__file__).parent / "templates" / "markdown.css"),
                                          width=800)
                await update_pidG(gid, msg['conversation_id'], msg['parent_id'])
                await cp.finish(MessageSegment.image(msg_pic))  # 给用户发送消息
        logger.info("无事发生")
    except httpx.ConnectError:
        await cp.send("网络错误，请[zr]联系管理员")
    except json.decoder.JSONDecodeError:
        await cp.send("异常：json.decoder.JSONDecodeError，随机BUG，不必惊慌")
    '''


# 新建数据库（仅管理员可操作）
async def NewDatabase():
    new_db = '''
                create table saveConversationsQQ
                (
                id integer primary key autoincrement,
                group_id text,
                qq text,
                conversation_id text,
                parent_id text
                );
            '''  # 创建数据表
    conn = sqlite3.connect(dbpath)  # 连接数据库
    cursor = conn.cursor()  # 获取游标
    cursor.execute(new_db)  # 执行指令
    conn.commit()  # 提交数据库
    conn.close()  # 关闭数据库
    logger.info("创建数据库完成~")


# 获取qq对应conversation_id 和 parent_id
async def get_cidQ(data) -> list:
    getid = '''
        SELECT *
        FROM saveConversationsQQ AS sCQ 
        WHERE qq = '{}'
    '''.format(data)
    conn = sqlite3.connect(dbpath)
    curses = conn.cursor()
    curses.execute(getid)
    datas = [curses.fetchone()]
    return datas


# 获取group对应conversation_id 和 parent_id
async def get_cidG(data: int) -> list:
    datas = []
    getid = f'''
        SELECT *
        FROM saveConversationsQQ AS sCQ 
        WHERE group_id = {data}
    '''
    conn = sqlite3.connect(dbpath)
    curses = conn.cursor()
    curses.execute(getid)
    for x in curses:
        datas.append(x)
        logger.info(x)
    conn.close()
    return datas


# 将未使用过的用户qq加入数据库
async def add_cidQ(qq: int, cid, pid):
    addid = f'''
        INSERT INTO saveConversationsQQ (qq,conversation_id,parent_id)
        VALUES ('{qq}','{cid}','{pid}')
    '''
    conn = sqlite3.connect(dbpath)
    curses = conn.cursor()
    curses.execute(addid)
    conn.commit()
    conn.close()


# 将未使用过的用户group加入数据库
async def add_cidG(group: int, cid, pid):
    addid = f'''
            INSERT INTO saveConversationsQQ (group_id,conversation_id,parent_id)
            VALUES ('{group}','{cid}','{pid}')
        '''
    conn = sqlite3.connect(dbpath)
    curses = conn.cursor()
    curses.execute(addid)
    conn.commit()
    conn.close()


# 发送完消息更新pid QQ
async def update_pidQ(qq, cid, pid):
    update = f'''
        UPDATE saveConversationsQQ
        SET parent_id = '{pid}',conversation_id = '{cid}'
        WHERE qq = '{qq}'
    '''
    conn = sqlite3.connect(dbpath)
    curses = conn.cursor()
    curses.execute(update)
    conn.commit()
    conn.close()


# 发送完消息更新pid group
async def update_pidG(gid, cid, pid):
    update = f'''
        UPDATE saveConversationsQQ
        SET parent_id = '{pid}',conversation_id = '{cid}'
        WHERE group_id = '{gid}'
    '''
    conn = sqlite3.connect(dbpath)
    curses = conn.cursor()
    curses.execute(update)
    conn.commit()
    conn.close()


# 获取新对话Q
async def new_converQ(qid):
    delcon = f'''
        DELETE FROM saveConversationsQQ
        WHERE qq = '{qid}'
    '''
    conn = sqlite3.connect(dbpath)
    curses = conn.cursor()
    curses.execute(delcon)
    conn.commit()
    conn.close()


# 获取新对话G
async def new_converG(gid):
    delcon = f'''
        DELETE FROM saveConversationsQQ
        WHERE group_id = '{gid}'
    '''
    conn = sqlite3.connect(dbpath)
    curses = conn.cursor()
    curses.execute(delcon)
    conn.commit()
    conn.close()


_help = '''==关于ChatGPT-v1.0==
请求示例：
cp + 你要说的话
eg：cp 鸡蛋
回复 cp 新建会话 则新建对话
注意事项：
如果当前会话为私人会话，则系统会根据您的qq生成一条独一无二的会话ID，凭借会话ID可联系上下文
如果当前会话为群聊，则整个群为一个会话
当前插件使用新库，如遇到bug请及时发送指令[zr]联系管理员

TODO：群聊/私聊 开始新会话'''
