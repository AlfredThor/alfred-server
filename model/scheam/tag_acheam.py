from typing import Optional
from pydantic import BaseModel


class Tag_scheam(BaseModel):
    id: Optional[int]
    tag_uuid: Optional[str] = None
    name: Optional[str] = None