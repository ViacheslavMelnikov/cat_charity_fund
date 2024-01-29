# ++++++++++++++++++++++++++++++++++++++++++++++
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, ForeignKey
from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime)
    close_date = Column(DateTime)
