from typing import Optional
# from datetime import datetime
from pydantic import BaseModel, Field, validator, PositiveInt, Extra


class Donation(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid

class DonationCreate(Donation):
    full_amount: PositiveInt()
    comment: Optional[str]

class DonationUpdate(Donation):
    
    @validator('full_amount')
    def full_amount_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Укажите сумму пожертвования!')
        return value


class DonationDB(DonationCreate):
    id: int

    class Config:
        orm_mode = True 