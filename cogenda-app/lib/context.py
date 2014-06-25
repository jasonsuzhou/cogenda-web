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
        #self.article_files = {}
        #self.sidebar_files = {}

    def load_settings(self, config_path):
        self.settings.load(config_path)

    def load_article_files(self, article_dir):
        self.article_files = locate('*.md', root=article_dir)

    def load_sidebar_files(self, sidebar_dir):
        self.sidebar_files = locate('*.md', root=sidebar_dir)

    def load_news_files(self, news_dir):
        self.news_files = locate('*.md', root=news_dir)

    def list_all_media(self):
        """docstring for list_all_media"""
        app_media = {}

        for app_path in self.app_paths.values():
            media_path = join(app_path, 'media')
            for file_name in locate("*.txt", "*.py", "*.css", "*.js", "*.rst", "*.html", "*.ini", root=media_path):
                if not is_file(file_name):
                    continue
                key = file_name.replace(media_path, '')
                app_media[key] = file_name
        return app_media
