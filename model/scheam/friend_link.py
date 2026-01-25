from typing import Optional
from pydantic import BaseModel


class Friend_link_scheam(BaseModel):
    id: Optional[int]
    friend_link_uuid: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str]
    is_visible: Optional[str] = None