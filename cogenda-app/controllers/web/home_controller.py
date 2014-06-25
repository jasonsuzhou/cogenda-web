#-*- coding:utf-8 -*-

from lib.controller import BaseController, route
from datetime import datetime
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
from datetime import datetime
import logging 
log = logging.getLogger(__name__)

class HomeController(BaseController):

    @route('/')
    def index(self):
        content = self.render_template('web/article/index.mdtxt')
        return self.render_template('web/index.html', content=content,news='IN PROGRESS', sidebar='IN PROGRESS')


    @route('/switch/:locale')
    def switch_locale(self, locale):
        refer = cherrypy.request.headers.get('Referer','/')
        cherrypy.tools.I18nTool.set_custom_language(locale) 
        self.redirect(refer)


    @route('/download/:resource_id')
    def download(self, resource_id):
        """Testing download & url with parameter"""
        log.debug("Download resource: %s" % resource_id);
        cherrypy.response.headers["Content-Type"] = "application/octet-stream"
        cd = 'attachment; filename="%s"' % resource_id
        cherrypy.response.headers["Content-Disposition"] = cd
        cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda-media.oss-cn-hangzhou.aliyuncs.com/media/123.png?Expires=1403359250&OSSAccessKeyId=DvSB6U5JdgjPj1Zr&Signature=vdtP0ldMD0yCskxmGcPxuF0oPuM%3D'
        #cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda.oss-cn-hangzhou.aliyuncs.com/static/js/cogenda.admin.js'
