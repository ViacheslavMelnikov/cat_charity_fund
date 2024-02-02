from typing import Optional
from datetime import datetime
from pydantic import BaseModel, PositiveInt, Extra


class Donation(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid

class DonationCreate(Donation):
    full_amount: PositiveInt()
    comment: Optional[str]


class DonationDB(DonationCreate):
    id: int
    user_id: Optional[int]
    comment: Optional[str]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True 
