#-*- coding:utf-8 -*-

from lib.controller import BaseController, route
from datetime import datetime
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
from datetime import datetime
from fuzzywuzzy import fuzz
import logging 
import os
import random

log = logging.getLogger(__name__)

class HomeController(BaseController):

    @route('/')
    def index(self):
        content = self.render_template('web/article/index.mdtxt')
        news = self.render_template('web/news/index.mdtxt')
        return self.render_template('web/index.html', 
                content=content, 
                news=news, 
                sidebar=self._retrieve_random_sidebar())


    @route('/article/:article_name')
    def serve_article(self, article_name):
        return self.render_template('web/index.html', 
                content=self._retrieve_optimized_article(article_name), 
                news=self.render_template('web/news/index.mdtxt'), 
                sidebar=self._retrieve_random_sidebar())


    @route('/news/:news_name')
    def serve_news(self, news_name):
        pass


    @route('/switch/:locale')
    def switch_locale(self, locale):
        refer = cherrypy.request.headers.get('Referer','/')
        cherrypy.tools.I18nTool.set_custom_language(locale) 
        self.redirect(refer)


    @route('/download/:resource_id')
    def serve_downloads(self, resource_id):
        """Testing download & url with parameter"""
        log.debug("Download resource: %s" % resource_id);
        cherrypy.response.headers["Content-Type"] = "application/octet-stream"
        cd = 'attachment; filename="%s"' % resource_id
        cherrypy.response.headers["Content-Disposition"] = cd
        cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda-media.oss-cn-hangzhou.aliyuncs.com/media/123.png?Expires=1403359250&OSSAccessKeyId=DvSB6U5JdgjPj1Zr&Signature=vdtP0ldMD0yCskxmGcPxuF0oPuM%3D'
        #cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda.oss-cn-hangzhou.aliyuncs.com/static/js/cogenda.admin.js'

    def _retrieve_random_sidebar(self):
        sidebar_files = self.context.sidebar_files.values()
        sidebar_choice = random.choice(sidebar_files)
        return self.render_template('web/sidebar/%s' %(sidebar_choice))


    def _retrieve_optimized_article(self, article_name):
        best_choice = 'index.mdtxt'
        best_ratio = None
        for (key, val) in self.context.article_files.items():
           article = os.path.splitext(val)[0] 
           ratio = fuzz.ratio(article_name, article)
           if not best_ratio:
               best_ratio = ratio
               best_choice = val

           if best_ratio < ratio:
               best_ratio = ratio
               best_choice = val

        best_choice = 'web/article/%s' %(best_choice)
        return self.render_template(best_choice)

    def _retrieve_optimized_news(self, news_name):
        pass
