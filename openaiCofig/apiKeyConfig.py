import nonebot
from nonebot import logger
'''
传入.env参数
'''
from typing import Optional
from pydantic import Extra, BaseModel
class Config(BaseModel, extra=Extra.ignore):
    openai_apikey: Optional[str] = None
    debug: bool = False
plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())

api_key = plugin_config.openai_apikey
