# -*- coding = utf-8 -*-
import json
import nonebot
from nonebot.adapters.onebot.v11 import  Event,  GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command, logger, on_keyword
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from paho.mqtt import client as mqtt_client

op_door = on_keyword({'开门'}, priority=10)

reg = on_command('注册', priority=11)

broker = '101.43.168.81'
port = 1883
topic = "OpenTheDoor"
# generate client ID with pub prefix randomly
client_id = 'QQBOT'


@op_door.handle()
async def _(event: Event):
    if isinstance(event, GroupMessageEvent):
        rooms = dict()
        try:
            with open('roomDATA.json', 'r') as f:
                content = f.read()
                rooms = json.loads(content)
                f.close()
        except Exception as e:
            logger.error(e)
            pass
        group = event.group_id
        logger.info(group)
        logger.info(type(group))
        if str(group) in rooms:
            await op_door.send("芝麻开门~（请稍等）")
            room = rooms[str(group)]
            client = connect_mqtt()
            publish(client, room)
            client.disconnect()
            await op_door.finish("门已打开~")
        else:
            await reg.finish("请注册宿舍后在使用~")
    else:
        await op_door.finish("请在您宿舍群中发送指令")
    logger.info("完毕")


@reg.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("reg_room", args)  # 如果用户发送了参数则直接赋值


@reg.got('reg_room', prompt="请问您要注册哪个房间呢？\n(输入 'help' 查看帮助)")
async def _(event: Event, reg_room=ArgPlainText('reg_room')):
    if isinstance(event, GroupMessageEvent):  # 如果时群聊
        rooms = dict()
        try:
            with open('roomDATA.json', 'r') as f:
                content = f.read()
                rooms = json.loads(content)
                f.close()
        except Exception as e:
            logger.error(e)
            pass
        group = event.group_id
        rooms[group] = reg_room
        with open('roomDATA.json', 'w') as f:
            b = json.dumps(rooms)
            f.write(b)
            f.close()
        await reg.send('完毕,' + '已将群 ' + str(group) + ' 注册为 ' + reg_room)


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, room):
    msg = "open"
    topic_new = topic + room
    logger.info(topic_new)
    result = client.publish(topic_new, msg)
    status = result[0]
