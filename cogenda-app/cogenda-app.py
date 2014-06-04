# -*- coding:utf-8 -*-

from lib.server import Server
from lib.fs import *
import sys
from os.path import join, dirname, abspath, exists, split

def main():

    init_files = locate("cogenda-app.ini")
    if not init_files:
        raise RuntimeError("No files called congenda-app.ini were found in the current directory structure")

    root_dir = abspath(dirname(init_files[0]))
    server = Server(root_dir=root_dir)

    try:
        server.start("cogenda-app.ini")
    except KeyboardInterrupt:
        server.stop()
    

if __name__ == '__main__':
    sys.exit(main())
