#-*- coding:utf-8 -*-


from lib.controller import BaseController, route
from datetime import datetime
from models import User
import cherrypy

class UserController(BaseController):

    @route('/')
    def index(self):
        """ testing SQLite and Jinja2 """
        user = User('Tim', '123', 'tang.jilong@gmail.com')
        cherrypy.request.db.add(user) 
        all_users = User.list(cherrypy.request.db);
        for temp_user in all_users:
            print temp_user.username
        return self.render_template('index.html', date=datetime.now());
