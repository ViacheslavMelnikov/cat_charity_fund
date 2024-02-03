from sqlalchemy import Column, ForeignKey, Integer, Text

from .charity_project import AbstractBaseModel


class Donation(AbstractBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
