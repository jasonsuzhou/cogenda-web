#-*- coding:utf-8 -*-


from lib.controller import BaseController, route
from datetime import datetime
from models import User
import cherrypy
from lib.i18ntool import ugettext as _

class AdminController(BaseController):

    @route('/admin')
    def index(self):

        #cherrypy.tools.I18nTool.set_custom_language('en_US') 'zh_CN'

        """ testing SQLite and Jinja2 """
        #user = User('Tim', '123', 'tang.jilong@gmail.com')
        #cherrypy.request.db.add(user)
        #all_users = User.list(cherrypy.request.db)
        #for temp_user in all_users:
        #    print temp_user.username
        
        return self.render_template('login.html', date=datetime.now(), hello=_('hello'))
