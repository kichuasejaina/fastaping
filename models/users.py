from models import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=False, nullable=True)
    last_name = Column(String(50), index=False, nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=False)


class Password(Base):
    __tablename__ = "password"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)
    password = Column(String(100), nullable=False)

# mysql+pymysql://root:Welcome-1@127.0.0.1:3306/testdb
