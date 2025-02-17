import datetime

from models import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True,nullable=False,autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)
