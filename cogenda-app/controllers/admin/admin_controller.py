#-*- coding:utf-8 -*-


from lib.controller import BaseController, route
from datetime import datetime
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
import json

import logging 
log = logging.getLogger(__name__)

class AdminController(BaseController):

    @route('/admin/auth-login')
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

    @route('/admin/users')
    @cherrypy.tools.json_out()
    def user_mgmt_data(self):
        all_users = User.list(cherrypy.request.db)
        users_in_json = []
        for user in all_users:
            users_in_json.append(self.jsonify_model(user))
        return users_in_json

    @route('/admin/fetch-user/:uid')
    @cherrypy.tools.json_out(content_type='application/json')
    def get_user_by_id(self, uid):
        user = User.get_by_uid(cherrypy.request.db, uid)
        print user
        user_in_json = self.jsonify_model(user)
        return user_in_json

    @route('/admin/create-user')
    @cherrypy.tools.json_out()
    def create_user(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_user = json.loads(rawbody)
        user = User(
                json_user['username'], 
                json_user['password'],
                json_user['company'],
                json_user['email'],
                json_user['mobile'],
                json_user['role'],
                json_user['resource'],
                json_user['notes'],
                json_user['active'],
                #TODO: remove this part with defaut datetime in SQLite3
                datetime(2014,6,16,12,12,12), 
                datetime(2014,6,16,12,12,12))
        temp_user = cherrypy.request.db.add(user)
        print temp_user
        return self.jsonify_model(user)

    @route('/admin/update-user')
    @cherrypy.tools.json_out()
    def update_user(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_user = json.loads(rawbody)
        user = User.update_by_uid(cherrypy.request.db, json_user['id'], json_user['company'])
        return self.jsonify_model(user)

    @route('/admin/delete-user/:uid')
    @cherrypy.tools.json_out(content_type='application/json')
    def destroy_user(self, uid):
        count = User.delete_by_uid(cherrypy.request.db, uid)
        return count

    @route('/admin/resources')
    @cherrypy.tools.json_out()
    def resource_mgmt_data(self):
        all_resources = Resource.list(cherrypy.request.db)
        resources_in_json = []
        for resource in all_resources:
            resources_in_json.append(self.jsonify_model(resource))
        return resources_in_json

    def jsonify_model(self, model):
        """ Returns a JSON representation of an SQLAlchemy-backed object.
        """
        json = {}

        columns = model._sa_class_manager.mapper.mapped_table.columns
        for col in columns:
            col_name = col.name
            col_val = getattr(model, col_name)
            if col_name == 'created_date' or col_name == 'updated_date':
                continue
            elif col_name == 'uploaded_date':
                json[col_name] = datetime.strftime(col_val, '%Y-%m-%d %H:%M:%S')
            elif col_name == 'role':
                json[col_name] = self.get_role_name(col_val)
            elif col_name == 'status':
                json[col_name] = self.get_resource_status(col_val)
            elif col_name == 'type':
                json[col_name] = self.get_resource_type(col_val)
            else:
                json[col_name] = col_val

        return json

    @staticmethod
    def get_resource_status(status):
        resource_status = 'Fail'
        if status == '1':
            resource_status = 'Successful'
        else:
            resource_status = 'Fail'
        return resource_status

    @staticmethod
    def get_resource_type(_type):
        resource_type = 'Restricted'
        if _type == '0':
            resource_type = 'Public'
        else:
            resource_type = 'Restricted'
        return resource_type

    @staticmethod
    def get_role_name(role_id):
        role_name = 'Resource'
        if role_id == '1':
            role_name = 'Resource'
        elif role_id == '2':
            role_name = 'Resource Owner'
        elif role_id == '3':
            role_name = 'Administrator'
        return role_name
