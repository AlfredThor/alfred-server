from typing import Optional
from pydantic import BaseModel


class Monthes_auth_scheam(BaseModel):
    '''客服添加'''
    work_type: Optional[str]
    serial: Optional[int]
    auth_name: Optional[str]
    equipment: Optional[str]
    user_name: Optional[str]


class Finance_scheam(BaseModel):
    card_info: Optional[str]