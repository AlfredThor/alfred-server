from typing import Optional
from pydantic import BaseModel


class Visit_log_schaem(BaseModel):
    id: Optional[int]
    visit_log_uuid: Optional[str] = None
    ip: Optional[str] = None
    path: Optional[str] = None
    access_time: Optional[str] = None