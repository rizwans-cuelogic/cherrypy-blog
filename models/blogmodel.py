import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import String, Integer,DateTime,Boolean
from models.usermodel import user,ORMBase 

class Blog(ORMBase):

	__tablename__ = 'blog'

	id = Column(Integer,primary_key=True)
	title = Column(String(540),nullable=False)
	content = Column(String(),nullable=False)
	published_date = Column(DateTime,default=datetime.datetime.utcnow)
	published = Column(Boolean)
	user_id = Column(Integer,ForeignKey('user.id'))
