import os
import cherrypy
import json
import pagecalc
from sqlalchemy import desc
from jinja2 import Environment,FileSystemLoader  
from helpers.register_helper import (check_empty_data,
									check_password_length,
									check_password_match)
from models.usermodel import User,Blog,Attachments
from .auth import require,check_credentials
from views.flashing import flash,render_template


env = Environment(loader = FileSystemLoader('./templates')) 

current_dir = os.path.dirname(os.path.abspath(__file__))

app_root =  os.path.abspath(os.path.join(current_dir, os.pardir))

class BlogClass(object):

	cp_config = {
		'tools.auth.on': True
	}

	@cherrypy.expose
	@require()
	def addblog(self,title=None,content=None,published_d=None,file_image=None):

		try:
			if cherrypy.request.method=="POST":
				
				email= cherrypy.request.login
				user = cherrypy.request.db.query(User).filter_by(email=email).first()
				if user:
					filename = file_image.filename
					target = os.path.join(app_root,"static/images")
					destination = os.path.join(target,filename)
					with open(destination,'wb') as out:
						while True:
							data = file_image.file.read(8192)
							if not data:
								break
							out.write(data)


					if published_d:
						blog = Blog(title=title,content=content,published_date=published_d,author=user)
					else:
						blog = Blog(title=title,content=content,author=user)

					filecontent = Attachments(filename=filename,file_path=destination,parent=blog)
					cherrypy.request.db.commit()
					flash("Blog Added Successfully.")
					raise cherrypy.HTTPRedirect('/user/home')				


			return render_template('add_blog.html',request= cherrypy.request,cherrypy=cherrypy)
		except:
			cherrypy.request.db.rollback()
			raise
	@cherrypy.expose
	@require()
	def listblog(self,page=1):

		page = int(page)
		email= cherrypy.request.login
		user = cherrypy.request.db.query(User).filter_by(email=email).first()

		blog =user.blogs.filter_by().order_by(desc(Blog.id)).all()
		paginator = pagecalc.Paginator(total = len(blog), by = 10)
		blogs = list(page,blog,limit=10)
		pages = paginator.paginate(page)

		return render_template('list_blog.html',blogs=blogs,paginator=pages,request=cherrypy.request,cherrypy=cherrypy)

	@cherrypy.expose
	def blog_detail(self,id=None):
		
		blog = cherrypy.request.db.query(Blog).filter_by(id = id).first()

		if blog:

			return render_template('detail_blog.html',blog=blog,request=cherrypy.request,cherrypy=cherrypy)


	@cherrypy.expose
	@require()
	def blog_edit(self,id=None,title=None,content=None,published_d=None,file_image=None):
		
		blog = cherrypy.request.db.query(Blog).filter_by(id = id).first()
		import pdb
		pdb.set_trace()
		if blog:

			if cherrypy.request.method == "POST":

				blog.title= title
				blog.content = ""
				blog.content = content

				if file_image.filename != '':
					filename = file_image.filename
					target = os.path.join(app_root,"static/images")
					destination = os.path.join(target,filename)
					with open(destination,'wb') as out:
						while True:
							data = file_image.file.read(8192)
							if not data:
								break
							out.write(data)
					filecontent = Attachments(filename=filename,file_path=destination,parent=blog)

				if published_d:
					blog.published_date = published_d

				cherrypy.request.db.commit()
				flash("Blog Saved Successfully.")
				raise cherrypy.HTTPRedirect('/blog/listblog')

			return render_template('edit_blog.html',blog=blog,request=cherrypy.request,cherrypy=cherrypy)

	@cherrypy.expose
	@require()
	def blog_delete(self,id=None):

		blog = cherrypy.request.db.query(Blog).filter_by(id = id).first()

		if blog:		

			cherrypy.request.db.delete(blog)
			cherrypy.request.db.commit()
			flash("Blog Deleted Successfully.")
			raise cherrypy.HTTPRedirect('/blog/listblog')


	@cherrypy.expose
	@require()
	def all_blog(self,page=1):

		page = int(page)
		email= cherrypy.request.login
		user = cherrypy.request.db.query(User).filter_by(email=email).first()

		blog = cherrypy.request.db.query(Blog).all()
		paginator = pagecalc.Paginator(total = len(blog), by = 10)
		blogs = list(page,blog,limit=10)
		pages = paginator.paginate(page)

		return render_template('all_blog.html',blogs=blogs,paginator=pages,request=cherrypy.request,cherrypy=cherrypy)


	@cherrypy.expose
	@require()
	def deleteimage(self,value=None):
		
		attachment = cherrypy.request.db.query(Attachments).filter_by(id=value).first()

		if attachment:

			cherrypy.request.db.delete(attachment)
			cherrypy.request.db.commit()

			message = {"success" : "Deleted successfully."}

			return json.dumps(message)
		
		else:
			message = {"Fail": "No found"}
			return json.dumps(message)


def list(page,data,limit):

	return data[(page - 1) * limit:page * limit]