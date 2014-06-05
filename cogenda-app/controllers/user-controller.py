#-*- coding:utf-8 -*-


from lib.controller import BaseController, route
from datetime import datetime

class UserController(BaseController):

    @route('/')
    def index(self)
        return self.render_template('index.html', date=datetime.now());
