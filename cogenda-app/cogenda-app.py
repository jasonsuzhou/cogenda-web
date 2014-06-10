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

def register_jinja(server):

    '''
    if not hasattr(server, '_static_hash'):
        server._static_hash = {}

    def static_url(filename):
        if server.testing:
            return filename

        if filename in server._static_hash:
            return server._static_hash[filename]

        with open(os.path.join(server.static_folder, filename), 'r') as f:
            content = f.read()
            hsh = hashlib.md5(content).hexdigest()

        server.logger.info('Generate %s md5sum: %s' % (filename, hsh))
        prefix = server.config.get('SITE_STATIC_PREFIX', '/static/')
        value = '%s%s?v=%s' % (prefix, filename, hsh[:5])
        server._static_hash[filename] = value
        return value

    @server.context_processor
    def register_context():
        return dict(static_url=static_url,)
    '''
    
def usage():
    print("usage: python cogenda-app/cogendap-app.py <settings_file>")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.exit(main(sys.argv[1]))
    else:
        usage()
        sys.exit(2)
