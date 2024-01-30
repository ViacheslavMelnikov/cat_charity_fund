# ++++++++++++++++++++++++++++++++++++++++++++++
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime
from app.core.db import Base
from datetime import datetime


class AbstractBaseModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)


class CharityProject(AbstractBaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
