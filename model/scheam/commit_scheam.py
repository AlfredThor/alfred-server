from typing import Optional
from pydantic import BaseModel


class Comment_scheam(BaseModel):
    id: Optional[int]
    comment_uuid: Optional[str] = None
    article_uuid: Optional[str] = None
    username_uuid: Optional[str] = None
    content: Optional[str] = None
    is_reviewed: Optional[str] = None