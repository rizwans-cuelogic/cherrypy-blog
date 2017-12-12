import cherrypy

from jinja2 import Environment,FileSystemLoader

env = Environment(loader = FileSystemLoader('./templates')) 

class RootClass(object):

	@property
	def db(self):
		return cherrypy.request.db

	@cherrypy.expose
	def index(self):
		template = env.get_template('index.html')
		return template.render(name="Rizwan")
