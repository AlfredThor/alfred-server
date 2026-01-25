from typing import Optional
from pydantic import BaseModel


class Category_scheam(BaseModel):
    id: Optional[int]
    category_uuid: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int]