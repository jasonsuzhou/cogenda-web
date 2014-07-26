# -*- coding:utf-8 -*-

from .lib import Server
from .lib.fs import locate
import sys
from os.path import dirname, abspath
import cherrypy
from .lib import BaseController

from .controllers.admin_controller import *
from .controllers.auth_controller import *
from .controllers.web_controller import *
from .controllers.ws_controller import *

class CogendaApp(Server):

    def __init__(self, settings_file):
        root_dir = self._retrieve_root_dir(settings_file)
        self.settings_file = settings_file
        super(CogendaApp, self).__init__(root_dir=root_dir)

    def bootstrap(self):
        dispatcher = self._register_routes(self)
        try:
            self.start(self.settings_file, dispatcher)
        except KeyboardInterrupt:
            self.stop()

    def _retrieve_root_dir(self, settings_file):
        init_files = locate(settings_file).keys()
        if not init_files:
            error = "No files called [%s] were found in the current directory structure" % settings_file
            raise RuntimeError(error)
        return abspath(dirname(init_files[0]))

    def _register_routes(self, server):
        """ Register router dispatchers """
        dispatcher = cherrypy.dispatch.RoutesDispatcher()
        for controller_type in BaseController.all():
            controller = controller_type(server=server)
            controller.register_routes(dispatcher)
        return dispatcher


if __name__ == '__main__':
    if len(sys.argv) == 2:
        cogendaApp = CogendaApp(sys.argv[1])
        cogendaApp.bootstrap()
    else:
        sys.exit(2)
