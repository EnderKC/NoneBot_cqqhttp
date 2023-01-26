# -*- coding = utf-8 -*-
from nonebot import on_message, on_keyword
from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent


cd = on_keyword({'菜单', 'cd'}, priority=10)
qg = on_keyword({'群管', 'qg'}, priority=11)
todo = on_keyword({'todo帮助'}, priority=12)


@cd.handle()
async def _(event: Event, bot: Bot):
    # await cd.finish(MessageSegment.text(_cd_con))
    await cd.finish(_cd_con)


@qg.handle()
async def _(event: Event, bot: Bot):
    # await cd.finish(MessageSegment.text(_cd_con))
    await qg.finish(_cd_qg)


@todo.handle()
async def _():
    await todo.finish(_todo_help)


_cd_con = '''    ===菜单===
    
1. [cd]    查看功能列表
2. [qndxx]    获取青年大学习截图
3. [fd]    复读内容
4. [jrrp]    进行运势测算
5. [资源]    查找资源
6. [qb]    QQ号查询
7. [st]    涩图
8. [oi]    AI生成图片
9. [cc]    以C++风格生成代码
10.[qg]    群管功能菜单
11.[zr]    与开发者交流
12.[xjj]   赠送小姐姐图片一张
13.[df]    赠送东方图片一张
14.[todo帮助]  查看todo提醒帮助
15.[mz]    妹子套图
16.[hs]    黑丝图片
17.[bs]    白丝图片

小学妹BOT'''

_cd_qg = '''===群管菜单===
禁言:
禁 @某人 时间（s）
禁 时间（s）@某人
禁 @某人 缺省时间则随机
解 @某人
    
全群禁言:
/all 
/all 解

改名片
改 @某人 名片

踢出:
踢 @某人
踢出并拉黑:
黑 @某人

撤回:
撤回 (回复某条消息即可撤回对应消息)'''

_todo_help = '''===todo帮助===
增加事项: '提醒'
eg：提醒我明天考试，提醒我12月22号考试

完成事项: '完成'
eg：完成考试

删除事项（支持正则表达式）: '删除', '去掉'
eg：删除考试

修改事项时间: '更正', '改'
eg：更正考试后天

查看当前待办: '获取todo' 

提示：支持每天时间提醒，请发送指令[zr]将你的账户添加到提醒队列'''
