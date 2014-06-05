#-*- coding:utf-8 -*-

import sys
import os
from os.path import join, abspath, dirname, splitext, split, exists

import cherrypy
from cherrypy.lib.static import serve_file
from cherrypy.process.plugins import PIDFile

from controller import BaseController
from context import Context
from cache import Cache
from fs import locate, is_file
from jinja2 import Environment, FileSystemLoader, PackageLoader, ChoiceLoader

import logging

from saplugin import SAEnginePlugin
from satool import SATool

class ServerStatus(object):
    Unknown = 0
    Starting = 1
    Started = 2
    Stopping = 3
    Stopped = 4

class Server(object):

    def __init__(self, root_dir, context=None):
        self.status = ServerStatus.Unknown
        self.root_dir = root_dir
        self.context = context or Context(root_dir=root_dir)
        self.template_filters = {}
        self.test_connection_error = None
        self.cache = None

    

    def get_server_settings(self):
        sets = self.context.settings

        return {
                'server.socket_host': sets.cogenda_app.host,
                'server.socket_port': sets.cogenda_app.as_int('port'),
                'server.thread_pool': sets.cogenda_app.as_int('threads'),
                'request.base': sets.cogenda_app.baseurl,
                'tools.encode.on': True, 
                'tools.encode.encoding': 'utf-8',
                'tools.decode.on': True,
                'tools.trailing_slash.on': True,
                'log.screen': sets.cogenda_app.as_bool('verbose'),
                'tools.sessions.on': True
                }


    def get_mounts(self, dispatcher):
        static_dir = os.path.join(self.root_dir,  'static')

        conf = {
                '/': {
                    'tools.staticdir.root': static_dir,
                    'request.dispatch': dispatcher,
                    'tools.db.on': True
                    },
                '/static': {
                    'tools.gzip.on': True,
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': ''},
                '/static/css': {
                    'tools.gzip.mime_types':['text/css'],
                    'tools.staticdir.dir': 'css'},
                '/static/js': {
                    'tools.gzip.mime_types': ['application/javascript'],
                    'tools.staticdir.dir': 'js'},
                '/static/img': {'tools.staticdir.dir': 'images'}
                }
        return conf


    def get_dispatcher(self):
        routes_dispatcher = cherrypy.dispatch.RoutesDispatcher()
        for controller_type in BaseController.all():
            controller = controller_type(server=self)
            controller.register_routes(routes_dispatcher)

        route_name = "healthcheck"
        controller = BaseController()
        controller.server = self
        routes_dispatcher.connect("healthcheck", "/healthcheck", controller=controller, action="healthcheck")

        dispatcher = routes_dispatcher
        return dispatcher


    def run_server(self, non_block=False):
        cherrypy.config.update(self.get_server_settings())
        dispatcher = self.get_dispatcher()
        mounts = self.get_mounts(dispatcher)
        self.app = cherrypy.tree.mount(None, config=mounts)

        """ Integrate with SQLAlchemy """
        protocol = self.context.settings.Db.protocol
        database = self.context.settings.Db.database
        conn_str = "%s:///%s" % (protocol, database)
        SAEnginePlugin(cherrypy.engine, conn_str).subscribe()
        cherrypy.tools.db = SATool()
        
        """ Integrate with Jinja2 """
        cherrypy.tools.jinja2env = Environment(loader = PackageLoader('cogenda-app', 'templates'))

        cherrypy.engine.start()
        if not non_block:
            cherrypy.engine.block()


    def start(self, config_path, non_block=False):
        self.status = ServerStatus.Starting

        self.context.load_settings(abspath(join(self.root_dir, config_path)))
        self.cache = Cache(size=1000, age="5s", log='cogenda-web.log')

        if self.context.settings.congend_web.as_bool('debug'):
            logging.basicConfig()
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
            logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)


        self.run_server(non_block)
        self.status = ServerStatus.Started


    def stop(self):
        self.status = ServerStatus.Stopping
        cherrypy.engine.exit()
        cherrypy.server.httpserver = None
        self.app_path = None
        self.status = ServerStatus.Stopped