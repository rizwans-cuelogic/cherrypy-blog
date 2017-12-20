import cherrypy

from jinja2 import Environment,FileSystemLoader
from .flashing import render_template 

env = Environment(loader = FileSystemLoader('./templates')) 

class RootClass(object):

	@cherrypy.expose
	def index(self):

		return render_template('index.html',request=cherrypy.request)

