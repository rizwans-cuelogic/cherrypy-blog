import cherrypy
import unittest
import requests
import os
import urllib
from cherrypy.test import helper
from contextlib import contextmanager
from views.index import RootClass
from views.user_management import UserClass
from views.blog_management import BlogClass
from models.usermodel import ORMBase
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin
from models.usermodel import User


sessions_dir = os.getcwd()+'/sessions'


@contextmanager
def run_server():
	cherrypy.engine.start()
	cherrypy.engine.wait(cherrypy.engine.states.STARTED)
	yield
	cherrypy.engine.exit()
	cherrypy.engine.block()

application_config = {
		'/':{'tools.staticdir.root':os.getcwd(),
			'tools.db.on':True,
			'tools.auth.on': True},
		'/static' : {'tools.staticdir.on': True,
					'tools.staticdir.dir':'static'
					},			

}

server_config = {
	'environment':'test_suite',
	'tools.sessions.on':True,
	"tools.sessions.storage_type":"file",
	"tools.sessions.storage_path":sessions_dir,
	"tools.sessions.timeout":180,
}

class UnitTestcase(helper.CPWebCase):

	# @classmethod
	# def setUpClass(cls):
	# 	cherrypy.config.update(server_config)
	# 	cherrypy.tools.db = SQLAlchemyTool()
	# 	sqlalchemy_plugin=SQLAlchemyPlugin(
	# 		cherrypy.engine, ORMBase, 'postgresql://postgres:admin123@localhost:5432/blog_test'
	# 	)
	# 	sqlalchemy_plugin.subscribe()
	# 	sqlalchemy_plugin.create()
	# 	cherrypy.root = RootClass()
	# 	cherrypy.root.user = UserClass()
	# 	cherrypy.root.blog = BlogClass()
	# 	cherrypy.tree.mount(cherrypy.root,'/',config=application_config)
	# 	cherrypy.engine.start()
	# 	cherrypy.engine.wait(cherrypy.engine.states.STARTED)
	# 	cls.cherrypy = cherrypy
	# 	print "setup class"
	# @classmethod
	# def tearDownClass(cls):
		
	# 	cherrypy.engine.exit()
	# 	cherrypy.engine.block()		
	# 	print "terdown"

	global session_id 
	session_id = list()
	def setup_server():

		cherrypy.config.update(server_config)
		cherrypy.tools.db = SQLAlchemyTool()
		sqlalchemy_plugin=SQLAlchemyPlugin(
			cherrypy.engine, ORMBase, 'postgresql://postgres:admin123@localhost:5432/blog_test'
		)
		sqlalchemy_plugin.subscribe()
		sqlalchemy_plugin.create()
		cherrypy.root = RootClass()
		cherrypy.root.user = UserClass()
		cherrypy.root.blog = BlogClass()
		cherrypy.tree.mount(cherrypy.root,'/',config=application_config)

	setup_server = staticmethod(setup_server)

	def test_a_home_page(self):

		rv = self.getPage('/')
		self.assertStatus('200 OK')

	def test_b_register_page(self):

	
		url = "/user/register"
		rv = self.getPage(url)
		self.assertStatus('200 OK')
		self.assertIn("Register",rv[2].decode())

	# def test_c_register_user(self):

	# 	url = "/user/register"
	# 	data = {
	# 		"username":"test",
	# 		"email":"test@example.com",
	# 		"password":"test1234",
	# 		"confirm_password":"test1234"
	# 	}
	# 	query_string = urllib.urlencode(data)
	# 	rv = self.getPage(url,method="POST",body=query_string)
	# 	self.assertStatus('200 OK')
	# 	self.assertIn("User Register Successfully",rv[2].decode())

	def test_d_register_user_exist(self):

		

		url = "/user/register"
		data = {
			"username":"test",
			"email":"test@example.com",
			"password":"test1234",
			"confirm_password":"test1234"
		}
		query_string = urllib.urlencode(data)
		rv = self.getPage(url,method="POST",body=query_string)
		self.assertStatus('200 OK')
		self.assertIn("User already exists",rv[2].decode())


	def test_e_login_invalid(self):

		url = "/user/login"
		data = {
			"email":"test@example.com",
			"password":"test12"
		}
		query_string = urllib.urlencode(data)
		rv = self.getPage(url,method="POST",body=query_string)
		self.assertStatus('200 OK')
		self.assertIn("Incorrect username or password.",rv[2].decode())
				

	def test_f_login_valid(self):

		url = "/user/login"
		data = {
			"email":"test@example.com",
			"password":"test1234"
		}
		query_string = urllib.urlencode(data)
		rv = self.getPage(url,method="POST",body=query_string)
		global session_id
		session_id.append(self.cookies[0])
		self.assertStatus(303)			

	def test_g_userprofile_valid(self):
		
		url = "/user/user_profile"
		data = {
			"gender":"Male",
			"Address":"123,test street"
		}
		query_string = urllib.urlencode(data)
		rv = self.getPage(url,headers=session_id,method="POST",body=query_string)
		self.assertStatus(303)
	
	def test_i_add_blog(self):

		
		url = "/blog/addblog"
		file = open('/home/alive/Pictures/brittany.jpg','rb')

		data = {
			"title":"test blog",
			"content":"test content",
			"file_image":file
		}
		query_string = urllib.urlencode(data)
		headers=[]
		headers.append(session_id[0])
		headers.append(session_id[1])
		headers.append(('Accept','multipart/form-data'))
		headers.append(('Content-Length','34; boundary=63c5979328c44e2c869349443a94200e' ))
		rv = self.getPage(url,method="POST",body=query_string)
		self.assertStatus(303)

	def test_i_edit_blog(self):

		
		url = "/blog/blog_edit/"+str(1)
		data = {
			"title":"test blog",
			"content":"test content",
			"file_image":''
		}
		query_string = urllib.urlencode(data)
		headers=[]
		headers.append(session_id[0])
		headers.append(session_id[1])
		rv = self.getPage(url,headers=headers,method="POST",body=query_string)
		self.assertStatus(200)	

	def test_i_delete_blog(self):

		url = "/blog/blog_delete/"+str(1)
		headers=[]
		headers.append(session_id[0])
		headers.append(session_id[1])
		rv = self.getPage(url,headers=headers)
		self.assertStatus('200 OK')


	def test_h_logout_valid(self):
		url = "/user/logout"
		rv = self.getPage(url)
		self.assertStatus(303)