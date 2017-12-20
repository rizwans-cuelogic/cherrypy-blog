import cherrypy
from models.usermodel import User


SESSION_KEY = '_cp_username'

def check_credentials(email, password,db):
    

    user = db.query(User).filter_by(email=email).first()

    if email == '' or password == '':
        return u"please fill the details."

    if user is None:
        return u"User Does not Exist."

    if user.password != password:
        return u"Incorrect username or password."
    

def check_auth(*args, **kwargs):

    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/user/login")
        else:
            raise cherrypy.HTTPRedirect("/user/login")
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):

    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate


