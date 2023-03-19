# -*- coding = utf-8 -*-


from nonebot.adapters.onebot.v11 import MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command, logger
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from pyChatGPT import ChatGPT
from pathlib import Path
from nonebot_plugin_htmlrender import (
    text_to_pic,
    md_to_pic,
    template_to_pic,
    get_new_page,
)

session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..KWtv3B0SmQqPutIs.ht1W-jlYfP6mFcyZY9GwTEbimlH6D9mWIFt9ByVveqtWM6uzFdHmvbIBjJV4v8phx9I2s1ZbZ_SyTRs1sRXTQyHM1NgTvCjq_A8DSEHwM9HZac6dOqkRN_WrUPV0LtIAnI6o955kLqc-p9oi9K2MfSyajdOmczUw-oCwmV8tltUPjrD4vzSI7Kc1UtBOqOvk6mFmOt47Grb7mjuy2MgEb0hoHYHuRiFAhO1cksvI4LCmLZe1G3p-bEVu2I-kHQ9Iet0tavBAK1maBVf5O1o61Z8iPw6pXTUEt4to4gVS6w5QsB_gNK6WA4s_QCrUzXifnwJ-AnDap8IGtkX3yANizcGI0wMrBF-nOdbyr2zNs0FRXYqOKCV2t5U69ZGzFa9Cq7P476HE2Y7Qwdmiu2oYAdfIFofk2y1g6U1FHG3VtfhUslKaHVaIUYU8FfPrgGMuteDbf7TX14aXQPFYHrjXMvTlaowa5oQquBGfSgQ14QaCyosxVGJDpYkt9wj9THQY-svvyuPM0vS8qotmNYOH-0l8K_P2uAciYl33TfWhqwzWSjBaNuFdeVQyIqpY7yhwqGJ6YUoAh8QnaWcihlroKseOkAiKxqtT5J9ajcr_YxzZrwRupbJeZM-X3u2Nu52TuxCYJqb1xC9lugLnFqn8j3cHb-oND2X5H2kFH-nlXIl5kMtxrooKB5JiYXBHlNQDkZZKoXmMoZl3tPN5uA9E4RiK5zeM--w_73rH-kFOnsVJiYbZz0Y_0rSnQhQMte_aF7ChQD3A72qJ2a7lukqmDTPkniKiWboNIQ7pccDDRHRtlzZFgPOJZYrei_7jjaKPzXbB0B-Xff42-0vLB8zGsQ8my0luSWhxdd4rbUwRmvdvFZvsh0UNf-LKzv86-EEJZYns78zZbANx-YKL_NBMiBciiTnmw7X-5aiZNkPIx6gE2j-PerAkYd-4Y8-hk529nqQq4fw5kxCvIiFEf1RcrrMZVKOTv6rZjfTmp2Uo4bvnZIDXA0EBnXpVjygBe821yYXWegDEoYJ4WFzjjiyf2KESHN6PdBAxZCJ1Gv3b-EwMB8EbeueHsM_Khy8J65-eDjCRmwHCCAz_bW_UkI71TXgQHvsOX8mGqCPGrEFp_SQyh9JpKsKfMVIkmL-eriLnWqZCV7AtNWVpl5hmDRnQTBi_4_xsWamH6lyif2BBgJcj0yvx4VG6C9c-xfMwhhY9og0BSLFJV8hqmuQLUxouv6BKgNV0XvUllRZjsz8Io3_CNwV6nNNATt_9m_sdlaHrirJBdPKKyh82vWWOZ8EoeXGbqeRNg1-7M_LWxmWBxeW3n45KGxWgDvQ7ZB2_a0d_htXc3gpRv7ha1BE1C9aLvC0lkLMSj8ra2jtPIZzAoRhpBYZY24LKQZ-uW3Aq7BjwtdOT9CmALd4pawVURC0y7US-8n9j7M9GupfqTwFkr78xFR4hLAAC7xKGMKarHrLCB-cprgJ8giOYxi6b89sW1743MU778oyxsXn7by3l__ZT5RH5QLSioeEvYGxwfpyZIVvf4lgwgkw6t3xqpcxLORjLhoFLASRqdnKqE4XEgd4-5yuI_vUcWTAzYyi3RHzl5VfzGGB6Ja_HE86si7_dlOChHGcfm5ZPAoLGTKUR6ig0nW1UAyp153uQpXgWwjTk7sFWT54PcGi8Al-PCvVpQkZYO24uzs_XQsoL76460AAAyRhQiVu-JRaM6WrDtFAKhP6X0TnlzUUM9eSMUROAEmUQIHwzJ66HBqEBq-_45Yspw9oZTMrxg5cDpiBM2624mRBqIjg01ROPWgY-vN2qgmuahxB7ymwztYRqulJUcOgTfTM9YudtdA34lo_q3qL4V4p_BmHAuMtg_f2iorBQ39tpVXptjT3ALeJATKlGTTwo6TENzzHLk06jtSxcHtKfTU1ldie8hX-m-F2HmW9bdOW83uMlKCuioZRiyg9ZXoSSfDP6kuHATC9Yz3zAhvdk38VcbaGu-Mzut4b2qGVbC7wwZkyvokia1iHUemtEH4Uqs8zlkTrT3VTJWqyLqD05Yl4NfC-3uqsoR3vv3Oq9PUBZ6U-lp9dJbJopBAzY23w-7_tH1xSt4o5fuyNhBlXxnxdjvs7XJwbvGSQVqATvcRYbu2cgXDdo3MVJxClme2qN9PhXMk_0MiimBv6QJ6oUh5bezCrANJGZSkCusep8M25Sk1rDZcl4G3H41TQhAvhonB9KHfTvMEJcug8meb6Ycn8c3z2ASqViOnLynAJUHAyrs8HusQzxu8-HLYoaHEPANZUKa9df_7GcDQ9W_5vMQsJNx1lGhoRJ1i6p1yvVcUyhKej-ns24-3L31Q.XDJnR3b6V-t_rECsSBoaSg'

gpt = on_command('gpt', aliases={'cgatgpt', 'ChatGPT'}, priority=10)


@gpt.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("text", args)  # 如果用户发送了参数则直接赋值


@gpt.got('text', prompt="请问您要发送的信息呢？\n(输入 'help' 查看帮助)")
async def _(bot: Bot, event: Event, text=ArgPlainText('text')):
    if 'help' in text:
        await gpt.finish(__help)
    await gpt.send('小学妹已收到！正在请求ChatGPT中~')
    api = ChatGPT(session_token)
    try:
        if text == '新建会话':
            api.reset_conversation()
            await gpt.finish('已新建会话，主人~', reply_message='true')
        try:
            msg = api.send_message(text)['message']
            msg = str(msg).strip('\n')
            i = 0
            while msg[-1] not in {'.', '?', '。', '!', '！', '？'} or i > 5:
                await gpt.send("机器人没有说完呢，继续请求~")
                tmp = api.send_message("继续")['message']
                tmp = str(tmp).strip('\n')
                msg = msg + '\n' + tmp
            msg_pic = await md_to_pic(msg,
                                      css_path=str(Path(__file__).parent / "templates" / "markdown.css"),
                                      width=500)
            await gpt.send(MessageSegment.image(msg_pic))
            logger.info(msg[-1])
            await gpt.finish('请求成功，主人~', reply_message='true')
        except IndexError:
            await gpt.finish("抱歉，发生异常，索引越界，请您稍后再试，或者[zr]联系管理员。", reply_message='true')
    except Exception as e:
        await gpt.send('异常:'+str(e)+'请[zr]联系管理人员，有时此消息为误发，请忽略')


__help = '''==ChatGPT==
触发条件：gpt+内容

注意事项：由于OpenAI官方加入Cloudflare的反机器人保护，以及不再使用request库，本机器人目前丧失了联系上下文的能力，每一次启动都是一次全新对话，未来功能还有待完善，尽情期待。

措施：当程序检测到ChatGPT的语句不完整时，自动发送“继续”让机器人说完话，如果因此耽误了您的猫娘计划，实在抱歉，我给您磕一个T_T'''
