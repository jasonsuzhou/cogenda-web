#-*- coding:utf-8 -*-


from lib.controller import BaseController, route
from datetime import datetime
from models import User
import cherrypy
from lib.i18ntool import ugettext as _

class UserController(BaseController):

    @route('/')
    def index(self):

        #cherrypy.tools.I18nTool.set_custom_language('en_US')

        """ testing SQLite and Jinja2 """
        user = User('Tim', '123', 'tang.jilong@gmail.com')
        cherrypy.request.db.add(user) 
        all_users = User.list(cherrypy.request.db)
        for temp_user in all_users:
            print temp_user.username
        
        return self.render_template('index.html', date=datetime.now(), hello=_('hello'))
