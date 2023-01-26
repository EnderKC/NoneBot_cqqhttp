# -*- coding = utf-8 -*-
from typing import Optional

from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    accept_invite: Optional[list] = None
    debug: bool = False
