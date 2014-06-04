#-*- coding:utf-8 -*-

import sys
import os
from os.path import join, abspath, dirname, splitext, split, exists

import cherrypy
from cherrypy.lib.static import serve_file
from cherrypy.process.plugins import PIDFile

from controller import BaseController
#from sqlalchemy_tool import metadata, session, mapper, configure_session_for_app
from context import Context
from cache import Cache
from fs import locate, is_file
from sqlalchemy.exc import DBAPIError
import logging

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
                'server.socket_host': sets.cogenda_web.host,
                'server.socket_port': sets.cogenda_web.as_int('port'),
                'server.thread_pool': sets.cogenda_web.as_int('threads'),
                'request.base': sets.cogenda_web.baseurl,
                'tools.encode.on': True, 
                'tools.encode.encoding': 'utf-8',
                'tools.decode.on': True,
                'tools.trailing_slash.on': True,
                'log.screen': sets.cogenda_web.as_bool('verbose'),
                'tools.sessions.on': True
                }


    def get_mounts(self, dispatcher):
        sets = self.context.settings

        protocol = self.context.settings.Db.protocol
        username = self.context.settings.Db.user
        password = self.context.settings.Db.password
        host = self.context.settings.Db.host
        port = int(self.context.settings.Db.port)
        database = self.context.settings.Db.database

        conn_str = self.connstr(protocol, username, password, host, port, database)
        static_dir = os.path.join(self.root_dir,  'static')

        conf = {
                '/': {
                    'tools.staticdir.root': static_dir,
                    'request.dispatch': dispatcher,
                    'tools.SATransaction.on': True,
                    'tools.SATransaction.dburi':conn_str, 
                    'tools.SATransaction.echo': sets.Ion.as_bool('verbose'),
                    'tools.SATransaction.convert_unicode': True
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


    def connstr(self, protocol, username, password, host, port, database):
        return "%s://%s:%s@%s:%d/%s" % (
                protocol,
                username,
                password,
                host,
                port,
                database
                )


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

        #self.context.use_db = self.test_connection()
        self.context.use_db = None

        if not self.context.use_db:
            cherrypy.config.update({'tools.SATransaction.on': False})

        cherrypy.engine.start()
        if not non_block:
            cherrypy.engine.block()


    """
    def test_connection(self):
        configure_session_for_app(self.app)
        try:
            session.execute("select 1 from dual")
        except DBAPIError, err:
            msg = '''\n\n============================ IMPORTANT ERROR ============================\nNo connection to the database could be made with the supplied parameters.\nPLEASE VERIFY YOUR CONFIG FILE AND CHANGE IT ACCORDINGLY.\n=========================================================================\n\n'''
            cherrypy.log.error(msg, 'DB')
            self.test_connection_error = err
            return False
        return True
    """


    def start(self, config_path, non_block=False):
        self.status = ServerStatus.Starting

        self.context.load_settings(abspath(join(self.root_dir, config_path)))
        self.cache = Cache(size=1000, age="5s", log=cherrypy.log)

        #self.app_paths = self.context.app_paths
        #self.app_modules = self.context.app_modules

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
