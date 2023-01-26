# -*- coding = utf-8 -*-
from typing import Optional

from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    master_id: Optional[str] = None
    debug: bool = False
