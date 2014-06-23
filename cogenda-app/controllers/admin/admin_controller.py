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

    @route('/admin/user-mgmt')
    def user_mgmt(self):
        self.is_authenticated()
        return self.render_template('admin/user-mgmt/user-container.html')

    @route('/admin/resource-mgmt')
    def resource_mgmt(self):
        self.is_authenticated()
        return self.render_template('admin/resource-mgmt/resource-container.html')

    @route('/admin/users')
    @cherrypy.tools.json_out()
    def user_mgmt_data(self):
        self.is_authenticated()
        all_users = User.list(cherrypy.request.db)
        users_in_json = []
        for user in all_users:
            users_in_json.append(self.jsonify_model(user))
        return users_in_json

    @route('/admin/fetch-user/:uid')
    @cherrypy.tools.json_out(content_type='application/json')
    def get_user_by_id(self, uid):
        self.is_authenticated()
        user = User.get_by_uid(cherrypy.request.db, uid)
        user_in_json = self.jsonify_model(user)
        return user_in_json

    @route('/admin/create-user')
    @cherrypy.tools.json_out()
    def create_user(self):
        self.is_authenticated()
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_user = json.loads(rawbody)

        # Check username
        username_checking = self.check_username(json_user['username'])
        if not (username_checking is None):
            return username_checking
        user = User(
                json_user['username'], 
                json_user['password'],
                json_user['company'],
                json_user['email'],
                json_user['mobile'],
                json_user['role'],
                json_user['resource'],
                json_user['notes'],
                json_user['active'])
        user.created_date = datetime.now()
        temp_user = cherrypy.request.db.add(user)
        print temp_user
        return self.jsonify_model(user)

    @route('/admin/update-user')
    @cherrypy.tools.json_out()
    def update_user(self):
        self.is_authenticated()
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_user = json.loads(rawbody)

        # Get original user by id
        origin_user = User.get_by_uid(cherrypy.request.db, json_user['id'])

        # Check username
        if origin_user.username != json_user['username']:
            username_checking = self.check_username(json_user['username'])
            if not (username_checking is None):
                return username_checking

        # Assemble user
        user = User(
                json_user['username'],
                json_user['password'],
                json_user['company'],
                json_user['email'],
                json_user['mobile'],
                json_user['role'],
                json_user['resource'],
                json_user['notes'],
                json_user['active'])
        user.updated_date = datetime.now()
        user = User.update_by_uid(cherrypy.request.db, json_user['id'], origin_user, user)
        return self.jsonify_model(user)

    @route('/admin/delete-user/:uid')
    @cherrypy.tools.json_out(content_type='application/json')
    def destroy_user(self, uid):
        self.is_authenticated()
        count = User.delete_by_uid(cherrypy.request.db, uid)
        return count

    @route('/admin/resources')
    @cherrypy.tools.json_out()
    def resource_mgmt_data(self):
        self.is_authenticated()
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
            else:
                json[col_name] = col_val
        return json

    def is_authenticated(self):
        auth = cherrypy.session.get('authenticated_user', None)
        if auth is None:
            self.redirect('/admin/login')

    def check_username(self, username):
        user = User.get_by_username(cherrypy.request.db, username)
        if not (user is None):
            return  u"The username is existing."