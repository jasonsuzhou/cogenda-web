#-*- coding:utf-8 -*-


import inspect
import sys
from os.path import join, dirname, splitext, split, exists

import cherrypy

from settings import Settings
from fs import locate, is_file 

class Context(object):
    def __init__(self, root_dir):
        #self.bus = Bus()
        self.settings = Settings(root_dir=root_dir)

    def load_settings(self, config_path):
        self.settings.load(config_path)

    def list_all_media(self):
        """docstring for list_all_media"""
        app_media = {}

        for app_path in self.app_paths.values():
            media_path = join(app_path, 'static')
            for file_name in locate("*.txt", "*.py", "*.css", "*.js", "*.rst", "*.html", "*.ini", root=media_path):
                if not is_file(file_name):
                    continue
                key = file_name.replace(media_path, '')
                app_media[key] = file_name
        return app_media
