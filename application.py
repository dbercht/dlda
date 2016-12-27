import tornado.wsgi
from server import application

application = tornado.wsgi.WSGIAdapter(application)