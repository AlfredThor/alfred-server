from typing import Optional
from pydantic import BaseModel


class Feedback_scheam(BaseModel):
    id: Optional[int]
    content: Optional[str] = None
    contact: Optional[str] = None
    is_handled: Optional[str] = None
    handle_note: Optional[str] = None
