import os
import cherrypy
from views.index import RootClass
from views.user_management import UserClass
from views.blog_management import BlogClass
from models.usermodel import ORMBase
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin


def start_server():
	
	sessions_dir = os.getcwd()+'/sessions'

	image_dir = os.getcwd() + '/static/images'

	if not os.path.exists(sessions_dir):
		os.makedirs(sessions_dir)

	if not os.path.exists(image_dir):
		os.makedirs(image_dir)

	server_config = {

		"server.socket_host":'0.0.0.0',
		"server.socket_port":int(os.environ.get('PORT', '5000')),
		"engine.autoreload.on": True,

		"tools.sessions.on":True,
		'tools.sessions.locking': 'early',
		"tools.sessions.storage_type":"file",
		"tools.sessions.storage_path":sessions_dir,
		"tools.sessions.timeout":180,

	}

	application_config = {
		'/':{'tools.staticdir.root':os.getcwd(),
			'tools.db.on':True,
			'tools.auth.on': True},
		'/static' : {'tools.staticdir.on': True,
					'tools.staticdir.dir':'static'
					},			

	}
	cherrypy.tools.db = SQLAlchemyTool()
	sqlalchemy_plugin=SQLAlchemyPlugin(
		cherrypy.engine, ORMBase, os.environ['DATABASE_URL'] 
	)
	#'postgresql://postgres:admin123@localhost:5432/blog_cherry'
	sqlalchemy_plugin.subscribe()
	sqlalchemy_plugin.create()
	cherrypy.config.update(server_config)
	cherrypy.root = RootClass()
	cherrypy.root.user = UserClass()
	cherrypy.root.blog = BlogClass()
	cherrypy.tree.mount(cherrypy.root,'/',config=application_config)
	cherrypy.engine.start()
	cherrypy.engine.block()



try:
	application=start_server()

except Exception as exe:
	print(exe)	