# -*- coding:utf-8 -*-

from lib.server import Server
from lib.fs import *
import sys
from os.path import join, dirname, abspath, exists, split
import cherrypy
import hashlib
import os
from lib.controller import BaseController

from controllers import *
from controllers.admin import *

def main(settings_file):

    init_files = locate(settings_file)
    if not init_files:
        raise RuntimeError("No files called setting file were found in the current directory structure")

    root_dir = abspath(dirname(init_files[0]))
    server = Server(root_dir=root_dir)
    dispatcher = register_routes(server)
    register_jinja(server)

    try:
        server.start(settings_file, dispatcher)
    except KeyboardInterrupt:
        server.stop()


def register_routes(server):
    """ Register router dispatchers """
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    for controller_type in BaseController.all():
        controller = controller_type(server=server)
        controller.register_routes(dispatcher)
    return dispatcher

def usage():
    print("usage: python cogenda-app/cogendap-app.py <settings_file>")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.exit(main(sys.argv[1]))
    else:
        usage()
        sys.exit(2)
