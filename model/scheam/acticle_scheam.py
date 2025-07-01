from typing import Optional
from pydantic import BaseModel


class Article_scheam(BaseModel):
    task_id: Optional[int]
    department_leader: Optional[str] = None
    administrator: Optional[str] = None
    issuer: Optional[str] = None
    reason: Optional[str]
    reviewer: Optional[str] = None
    delay_time: Optional[str] = None
    user_auth_uuid: Optional[str]
    user_auth_name: Optional[str]
    user_auth_conpany_name: Optional[str]