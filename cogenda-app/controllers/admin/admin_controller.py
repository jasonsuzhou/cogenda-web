#-*- coding:utf-8 -*-


from lib.controller import BaseController, route
from datetime import datetime
from models import User, Resource
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
        
        return self.render_template('admin/security/login-user.html', date=datetime.now(), hello=_('hello'))

    @route('/admin/user-mgmt')
    def user_mgmt(self):
        return self.render_template('admin/user-mgmt/user-container.html')

    @route('/admin/resource-mgmt')
    def resource_mgmt(self):
        return self.render_template('admin/resource-mgmt/resource-container.html')

    @route('/admin/user-mgmt-data')
    @cherrypy.tools.json_out()
    def user_mgmt_data(self):
        all_users = User.list(cherrypy.request.db)
        users_in_json = []
        #print all_users
        for user in all_users:
            users_in_json.append(self.to_json(user))
        return users_in_json

    @route('/admin/resource-mgmt-data')
    @cherrypy.tools.json_out()
    def resource_mgmt_data(self):
        all_resources = Resource.list(cherrypy.request.db)
        resources_in_json = []
        #print Resource
        for resource in all_resources:
            print resources_in_json
            resources_in_json.append(self.to_json(resource))
        return resources_in_json

    def to_json(self, model):
        """ Returns a JSON representation of an SQLAlchemy-backed object.
        """
        json = {}

        columns = model._sa_class_manager.mapper.mapped_table.columns
        for col in columns:
            if col.name == 'upload_date':
                json[col.name] = datetime.strftime(getattr(model, col.name), '%Y-%m-%d %H:%M:%S')
            else:
                json[col.name] = getattr(model, col.name)

        return json