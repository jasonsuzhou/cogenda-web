# -*- coding:utf-8 -*-

from cherrypy import wsgiserver
import cherrypy
from lib.server import Server
# Unsubscribe the default server

cherrypy.server.unsubscribe()

server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8001), app, numthreads=30)
server.start()

