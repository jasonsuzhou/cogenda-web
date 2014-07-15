#-*- coding:utf-8 -*-

from settings import Settings
from fs import locate


class Context(object):
    def __init__(self, root_dir):
        self.settings = Settings(root_dir=root_dir)

    def load_settings(self, config_path):
        self.settings.load(config_path)

    def load_article_files(self, article_dir):
        self.article_files = locate('*.md', root=article_dir)

    def load_sidebar_files(self, sidebar_dir):
        self.sidebar_files = locate('*.md', root=sidebar_dir)

    def load_news_files(self, news_dir):
        self.news_files = locate('*.md', root=news_dir)
