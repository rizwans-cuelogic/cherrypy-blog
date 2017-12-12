import os
import cherrypy
from views.index import RootClass
from models.usermodel import ORMBase
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin


def start_server():

	sessions_dir = os.getcwd()+'/sessions'

	if not os.path.exists(sessions_dir):
		os.makedirs(sessions_dir)

	server_config = {

		"server.socket_host":'0.0.0.0',
		"server.socket_port":8095,
		"engine.autoreload.on": False,

		"tools.sessions.on":True,
		"tools.sessions.storage_type":"file",
		"tools.sessions.storage_path":sessions_dir,
		"tools.sessions.timeout":180
	}

	application_config = {
		'/':{'tools.staticdir.root':os.getcwd()},
		'/static' : {'tools.staticdir.on': True,
					'tools.staticdir.dir':'static'
					}
	}
	cherrypy.tools.db = SQLAlchemyTool()
	SQLAlchemyPlugin(
		cherrypy.engine, ORMBase, 'postgresql://postgres:admin123@localhost:5432/blog_cherry'
	)
	cherrypy.config.update(server_config)
	cherrypy.tree.mount(RootClass(),'/',config=application_config)
	cherrypy.engine.start()



try:
	application=start_server()

except Exception as exe:
	print exe	