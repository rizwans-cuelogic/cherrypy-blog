from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer

ORMBase = declarative_base()


class User(ORMBase):
	__tablename__ = 'user'
	
	id = Column(Integer,primary_key=True)
	username = Column(String(64),index=True,unique=True)
	email = Column(String(120),index=True,unique=True)
	contact = Column(String(12),nullable=True)
	Address = Column(String(540),nullable=True)
	Gender = Column(String(10),nullable=True)
	password = Column(String(128))
	