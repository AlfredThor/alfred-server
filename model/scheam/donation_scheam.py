from typing import Optional
from pydantic import BaseModel


class Donation_scheam(BaseModel):
    id: Optional[int]
    amount: Optional[str] = None
    donor_name: Optional[str] = None
    message: Optional[str] = None
    article_id: Optional[str] = None
    author_id: Optional[str] = None