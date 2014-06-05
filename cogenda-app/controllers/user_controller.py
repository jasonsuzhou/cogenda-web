#-*- coding:utf-8 -*-


from lib.controller import BaseController, route
from datetime import datetime
from models import User
import cherrypy

class UserController(BaseController):

    @route('/')
    def index(self):
        user = User('Tim', '123', 'tang.jilong@gmail.com')
        #cherrypy.request.db.add(user) 
        return self.render_template('index.html', date=datetime.now());
