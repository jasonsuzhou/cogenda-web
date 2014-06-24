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
        #cherrypy.tools.I18nTool.set_custom_language('en_US') 'zh_CN'
        """ testing SQLite and Jinja2 """
        all_users = User.list(cherrypy.request.db)
        for temp_user in all_users:
            print temp_user.username
        return self.render_template('web/home.html')


    @route('/download/:resource_id')
    def download(self, resource_id):
        """Testing download & url with parameter"""
        log.debug("Download resource: %s" % resource_id);
        cherrypy.response.headers["Content-Type"] = "application/octet-stream"
        cd = 'attachment; filename="%s"' % resource_id
        cherrypy.response.headers["Content-Disposition"] = cd
        cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda-media.oss-cn-hangzhou.aliyuncs.com/media/123.png?Expires=1403359250&OSSAccessKeyId=DvSB6U5JdgjPj1Zr&Signature=vdtP0ldMD0yCskxmGcPxuF0oPuM%3D'
        #cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda.oss-cn-hangzhou.aliyuncs.com/static/js/cogenda.admin.js'
