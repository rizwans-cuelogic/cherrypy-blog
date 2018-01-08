import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import String, Integer,DateTime,Boolean,LargeBinary
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
	user_comments = relationship('Comment', backref='commentator',cascade="all,delete",lazy='dynamic')

class Blog(ORMBase):

	__tablename__ = 'blog'

	id = Column(Integer,primary_key=True)
	title = Column(String(540),nullable=False)
	content = Column(String(),nullable=False)
	published_date = Column(DateTime,default=datetime.datetime.utcnow)
	published = Column(Boolean)
	user_id = Column(Integer,ForeignKey('user.id'))
	files = relationship('Attachments',backref='parent',cascade='all,delete',lazy='dynamic')
	comments = relationship('Comment',backref='blog',cascade="all,delete",lazy='dynamic')

class Attachments(ORMBase):

	__tablename__ = 'attachments'

	id = Column(Integer,primary_key=True)
	filename = Column(String(540),nullable=False)
	file_path = Column(String(540))
	user_id = Column(Integer,ForeignKey('user.id'))
	blog_id = Column(Integer,ForeignKey('blog.id'))


class Comment(ORMBase):

	__tablename__ = 'comment'

	id = Column(Integer,primary_key=True)
	content = Column(String(),nullable=False)
	created = Column(DateTime,default=datetime.datetime.utcnow)
	user_id = Column(Integer,ForeignKey('user.id'))
	blog_id = Column(Integer,ForeignKey('blog.id'))
	parent = Column(Integer,ForeignKey('comment.id'),nullable=True)
	cm_replies = relationship('Comment',remote_side=[id],backref='replies',cascade="all,delete",lazy="joined")
