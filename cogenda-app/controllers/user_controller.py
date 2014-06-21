#-*- coding:utf-8 -*-


from lib.controller import BaseController, route
from datetime import datetime
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
from cherrypy.lib.static import serve_file
from datetime import datetime

import logging 
log = logging.getLogger(__name__)

class UserController(BaseController):

    @route('/')
    def index(self):

        #cherrypy.tools.I18nTool.set_custom_language('en_US') 'zh_CN'
        """ testing SQLite and Jinja2 """
        user = User('Tim', '123', 'Arctic INC.', 'tang.jilong@gmail.com', '1234567890', '1', '', 'This is notes~', 1, datetime(2014,6,16,12,12,12), datetime(2014,6,16,12,12,12))
        cherrypy.request.db.add(user) 
        all_users = User.list(cherrypy.request.db)
        for temp_user in all_users:
            print temp_user.username

        resource = Resource('jd.setup.v001.doc', '1', 'AliYun', 'http://asdfsafsadfsdafsdafsdafsdafsadfsdaf', 1, datetime(2014,6,16,12,12,12), 1)
        cherrypy.request.db.add(resource)
        all_resources = Resource.list(cherrypy.request.db)
        for temp_user in all_resources:
            print temp_user.name

        resource = Resource('jd.setup.v001.doc', '1', 'AWS S', 'http://12433456346346343456346534565434563', 1, datetime(2014,6,16,12,12,12), 1)
        cherrypy.request.db.add(resource)
        all_resources = Resource.list(cherrypy.request.db)
        for temp_user in all_resources:
            print temp_user.name
        
        return self.render_template('index.html', date=datetime.now(), hello=_('hello'))

    @route('/download/:resource_id')
    def download(self, resource_id):
        """Testing download & url with parameter"""
        log.debug("Download resource: %s" % resource_id);
        #cherrypy.response.headers["Content-Type"] = "application/x-download"
        cherrypy.response.headers["Content-Type"] = "application/octet-stream"
        #cd = 'attachment; filename="%s"' % resource_id
        #cherrypy.response.headers["Content-Disposition"] = cd
        #cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda-media.oss-cn-hangzhou.aliyuncs.com/media/123.png?Expires=1403348476&OSSAccessKeyId=DvSB6U5JdgjPj1Zr&Signature=Y6uRVDJurzEvJ2i7LTnjZND95es%3D'
        cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda.oss-cn-hangzhou.aliyuncs.com/static/js/cogenda.admin.js'
        #return serve_file(filepath, "application/x-download", "attachment")
        return cherrypy.response
