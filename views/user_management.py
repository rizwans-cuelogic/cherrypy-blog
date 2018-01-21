import cherrypy
import pagecalc
from sqlalchemy import desc
from jinja2 import Environment,FileSystemLoader
from .index import RootClass  
from helpers.register_helper import (check_empty_data,
									check_password_length,
									check_password_match)
from models.usermodel import User,Blog
from .auth import require,check_credentials
from .flashing import flash,render_template
from .blog_management import list

SESSION_KEY = '_cp_username'


class UserClass:
	
	_cp_config = {

		'tools.auth.on': True
	}

	@cherrypy.expose
	def login(self,email=None,password=None):
		
		template = 'login_user.html'
		
		if cherrypy.request.method == 'POST':
			
			error = check_credentials(email,password,cherrypy.request.db)

			if error:
				return render_template(template,error=error,request=cherrypy.request,cherrypy=cherrypy)
	
			cherrypy.session[SESSION_KEY] = cherrypy.request.login = email
			raise cherrypy.HTTPRedirect("/user/home")	
			
		return render_template(template,request=cherrypy.request,cherrypy=cherrypy)

	@cherrypy.expose
	def register(self,username=None,
				email=None,
				password=None,
				confirm_password=None):

		try:
			template = 'register.html'

			if cherrypy.request.method=="POST":

				if not (check_empty_data(username,email,password,confirm_password)):

					return render_template(template,error = "Please Fill All The Details",
											request=cherrypy.request,cherrypy=cherrypy)

				if not (check_password_length(password)):

					return render_template(template,password_error = "Password Should Be 6 Character Long",
											request=cherrypy.request,cherrypy=cherrypy)

				if not(check_password_match(password,confirm_password)):
					
					return render_template(template,password_error = "Password And Confirm Password Should Be Same",
											request=cherrypy.request,cherrypy=cherrypy)


				user = cherrypy.request.db.query(User).filter_by(email = email).first()
				
				if user:
					return render_template(template,error = "User already exists",
											request=cherrypy.request,cherrypy=cherrypy)
				user = User(username=username,email=email,password=password)

				cherrypy.request.db.add(user)
				cherrypy.request.db.commit()										
				template = 'login_user.html'
				return render_template(template,register_success="User Register Successfully.",
										request=cherrypy.request,cherrypy=cherrypy)			

			return render_template(template,request=cherrypy.request,cherrypy=cherrypy)

		except:
			cherrypy.request.db.rollback()
			raise

	@cherrypy.expose
	def logout(self):

		sess = cherrypy.session
		email = sess.get(SESSION_KEY, None)
		sess[SESSION_KEY] = None
		if email:
			cherrypy.request.login = None
			
		flash("User logout successfully")
		raise cherrypy.HTTPRedirect("/")



	@cherrypy.expose
	@require()
	def home(self,page=1):

		page = int(page)
		email= cherrypy.request.login
		user = cherrypy.request.db.query(User).filter_by(email=email).first()

		blog = cherrypy.request.db.query(Blog).filter_by().order_by(desc(Blog.id)).all()
		paginator = pagecalc.Paginator(total = len(blog), by = 10)
		blogs = list(page,blog,limit = 10)
		pages = paginator.paginate(page)

		template ='home.html'
		return render_template(template,blogs=blogs,paginator=pages,request=cherrypy.request,cherrypy=cherrypy)


	@cherrypy.expose
	@require()
	def user_profile(self,username=None,gender=None,email=None,contact=None,Address=None):
		
		try:
			email= cherrypy.request.login
			user = cherrypy.request.db.query(User).filter_by(email=email).first()

			
			if cherrypy.request.method == "POST":
				
				user.username=username
				user.email = email
				user.contact = contact
				user.Address = Address
				cherrypy.request.db.commit()
				flash("User profile Updated Successfully")
				raise cherrypy.HTTPRedirect("/user/user_profile")

			return render_template('profile.html',request=cherrypy.request,user=user,cherrypy=cherrypy)

		except:

			cherrypy.request.db.rollback()
			raise

