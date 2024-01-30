# ++++++++++++++++++++++++++++++++++++++++++++++
from sqlalchemy import Column, Text, Integer, ForeignKey
from .charityproject import AbstractBaseModel

class Donation(AbstractBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
