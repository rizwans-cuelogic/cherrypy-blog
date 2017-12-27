import cherrypy
import pagecalc
from sqlalchemy import desc
from jinja2 import Environment,FileSystemLoader
from .flashing import render_template 
from models.usermodel import User,Blog
from .auth import require,check_credentials
from .blog_management import list

env = Environment(loader = FileSystemLoader('./templates')) 

class RootClass(object):

	@cherrypy.expose
	
	def index(self,page=1):
		
		page = int(page)
		email= cherrypy.request.login
		user = cherrypy.request.db.query(User).filter_by(email=email).first()

		blog = cherrypy.request.db.query(Blog).filter_by().order_by(desc(Blog.id)).limit(10).all()
		paginator = pagecalc.Paginator(total = len(blog), by = 10)
		blogs = list(page,blog,limit=10)
		pages = paginator.paginate(page)

		return render_template('index.html',blogs=blogs,paginator=pages,request=cherrypy.request,cherrypy=cherrypy)

