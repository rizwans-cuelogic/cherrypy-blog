import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import String, Integer,DateTime,Boolean
from sqlalchemy.orm import relationship
# from .blogmodel import Blog

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
	blogs = relationship('Blog',backref='author',cascade='all,delete',lazy='dynamic')

class Blog(ORMBase):

	__tablename__ = 'blog'

	id = Column(Integer,primary_key=True)
	title = Column(String(540),nullable=False)
	content = Column(String(),nullable=False)
	published_date = Column(DateTime,default=datetime.datetime.utcnow)
	published = Column(Boolean)
	user_id = Column(Integer,ForeignKey('user.id'))
