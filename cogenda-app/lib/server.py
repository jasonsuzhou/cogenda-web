#-*- coding:utf-8 -*-

import sys
import os
from os.path import join, abspath, dirname, splitext, split, exists

import cherrypy
from cherrypy.lib.static import serve_file
from cherrypy.process.plugins import Daemonizer, PIDFile

from controller import BaseController
from context import Context
from fs import locate, is_file
from cherrypy.process.plugins import PIDFile

from saplugin import SAEnginePlugin
from satool import SATool

import logging
from logconfig import init_logging
from cherrypy import wsgiserver

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


    def get_server_settings(self):
        sets = self.context.settings

        return {
                #'server.socket_host': sets.cogenda_app.host,
                #'server.socket_port': sets.cogenda_app.as_int('port'),
                #'server.thread_pool': sets.cogenda_app.as_int('threads'),
                'request.base': sets.cogenda_app.baseurl,
                'tools.encode.on': True, 
                'tools.encode.encoding': 'utf-8',
                'tools.decode.on': True,
                'tools.trailing_slash.on': True,
                'log.screen': sets.cogenda_app.as_bool('verbose'),
                'tools.sessions.on': True,
                'tools.sessions.storage_type': 'ram',
                'tools.sessions.timeout': 3600,
                'tools.I18nTool.on': True,
                'tools.I18nTool.default': sets.cogenda_app.default_locale, 
                'tools.I18nTool.mo_dir': os.path.join(os.path.abspath(os.curdir), sets.cogenda_app.app_name ,'i18n'), 
                'tools.I18nTool.domain': sets.cogenda_app.app_name,
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
                '/static/img': {'tools.staticdir.dir': 'images'},
                '/static/fonts': {'tools.staticdir.dir': 'fonts'}
                }
        return conf


    def get_dispatcher(self, dispatcher):
        route_name = "healthcheck"
        controller = BaseController()
        controller.server = self
        dispatcher.connect("healthcheck", "/healthcheck", controller=controller, action="healthcheck")

        #dispatcher = routes_dispatcher
        return dispatcher


    def run_server(self, dispatcher, non_block=False):
        cherrypy.config.update(self.get_server_settings())
        dispatcher = self.get_dispatcher(dispatcher)
        mounts = self.get_mounts(dispatcher)
        self.app = cherrypy.tree.mount(None, config=mounts)

        """ Integrate with SQLAlchemy """
        protocol = self.context.settings.Db.protocol
        database = self.context.settings.Db.database
        conn_str = "%s:///%s" % (protocol, database)
        SAEnginePlugin(cherrypy.engine, conn_str).subscribe()
        cherrypy.tools.db = SATool()

        """ Integrate with embed WSGI server """
        # Unsubscribe the default server
        cherrypy.server.unsubscribe()
        self.server = cherrypy._cpserver.Server()
        self.server.socket_host = self.context.settings.cogenda_app.host
        self.server.socket_port = self.context.settings.cogenda_app.as_int('port')
        self.server.thread_pool = self.context.settings.cogenda_app.as_int('threads')
        # Subscribe this server
        self.server.subscribe()

        cherrypy.engine.start()
        if not non_block:
            cherrypy.engine.block()


    def start(self, config_path, dispatcher, non_block=False):
        self.status = ServerStatus.Starting
        self.context.load_settings(abspath(join(self.root_dir, config_path)))

        """ Init cogenda app logging """
        log_dir = self.context.settings.cogenda_app.log_dir
        log_file = self.context.settings.cogenda_app.log_file
        is_debug = self.context.settings.cogenda_app.as_bool('debug')

        if is_debug:
            init_logging(log_dir, log_file, logging.DEBUG);
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
            logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)
        else:
            init_logging(log_dir, log_file, logging.ERROR);

        if self.context.settings.cogenda_app.as_bool('daemon'):
            Daemonizer(cherrypy.engine).subscribe()

        if self.context.settings.cogenda_app.pid_file:
            PIDFile(cherrypy.engine, self.context.settings.cogenda_app.pid_file).subscribe()

        self.run_server(dispatcher, non_block)
        self.status = ServerStatus.Started


    def stop(self):
        self.status = ServerStatus.Stopping
        cherrypy.engine.exit()
        cherrypy.server.httpserver = None
        self.server.stop()
        self.app_path = None
        self.status = ServerStatus.Stopped
