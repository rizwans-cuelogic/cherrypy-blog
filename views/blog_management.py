import cherrypy

from jinja2 import Environment,FileSystemLoader
from .index import RootClass  
from helpers.register_helper import (check_empty_data,
									check_password_length,
									check_password_match)
from models.usermodel import User,Blog
from .auth import require,check_credentials
from views.flashing import flash,render_template

from .user_management import SESSION_KEY

env = Environment(loader = FileSystemLoader('./templates')) 


class BlogClass(object):

	cp_config = {
		'tools.auth.on': True
	}

	@cherrypy.expose
	@require()
	def addblog(self,title=None,content=None,published_d=None):

		if cherrypy.request.method=="POST":
			email= cherrypy.request.login
			user = cherrypy.request.db.query(User).filter_by(email=email).first()
			if user:
				if published_d:
					blog = Blog(title=title,content=content,published_date=published_d,author=user)
				else:
					blog = Blog(title=title,content=content,author=user)

				cherrypy.request.db.commit()
				flash("Blog Added Successfully.")
				raise cherrypy.HTTPRedirect('/user/home')				


		return render_template('add_blog.html',request= cherrypy.request)
		

	@cherrypy.expose
	@require()
	def listblog(self):
		
		email= cherrypy.request.login
		user = cherrypy.request.db.query(User).filter_by(email=email).first()

		blogs =user.blogs.all()
		
		return render_template('list_blog.html',blogs=blogs,request=cherrypy.request)

	@cherrypy.expose
	@require()
	def blog_detail(self,id=None):
		

		blog = cherrypy.request.db.query(Blog).filter_by(id = id).first()

		if blog:

			return render_template('detail_blog.html',blog=blog,request=cherrypy.request)


	@cherrypy.expose
	@require()
	def blog_edit(self,id=None,title=None,content=None,published_d=None):
		import pdb
		pdb.set_trace()

		blog = cherrypy.request.db.query(Blog).filter_by(id = id).first()

		if blog:

			return render_template('edit_blog.html',blog=blog,request=cherrypy.request)

		if cherrypy.request.method == "POST":

			blog.title= title
			blog.content = content

			if published_d:
				blog.published_date = published_d

			cherrypy.request.db.commit()	 


