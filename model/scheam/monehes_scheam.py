from typing import Optional
from decimal import Decimal
from pydantic import BaseModel


class Monthes_auth_scheam(BaseModel):
    '''客服添加'''
    fuk_dan: Optional[Decimal] = None
    work_type: Optional[str] = None
    user_bank_name: Optional[str] = None
    user_bank_number: Optional[str] = None
    user_name: Optional[str] = None
    card_type: Optional[str] = None
    card_country: Optional[str] = None
    card_code: Optional[str] = None
    card_balance: Optional[Decimal] = None
    card_rate: Optional[Decimal] = None
    auth_name: Optional[str] = None
    equipment: Optional[str] = None
    handling: Optional[Decimal] = None


class Finance_scheam(BaseModel):
    card_info: Optional[str]