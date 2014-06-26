#-*- coding:utf-8 -*-


from lib.controller import BaseController, route, authenticated
from datetime import datetime
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
import json
import hmac
from sqlalchemy.exc import DBAPIError

import logging 
log = logging.getLogger(__name__)

class AdminController(BaseController):

    @route('/admin/user-mgmt')
    @authenticated
    def user_mgmt(self):
        return self.render_template('admin/user-mgmt/user-container.html')

    @route('/admin/resource-mgmt')
    @authenticated
    def resource_mgmt(self):
        return self.render_template('admin/resource-mgmt/resource-container.html')

    @route('/admin/users')
    @cherrypy.tools.json_out()
    @authenticated
    def user_mgmt_data(self):
        all_users = User.list(cherrypy.request.db)
        users_in_json = []
        for user in all_users:
            users_in_json.append(self.jsonify_model(user))
        return users_in_json

    @route('/admin/fetch-user/:uid')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def get_user_by_id(self, uid):
        user = User.get_by_uid(cherrypy.request.db, uid)
        user_in_json = self.jsonify_model(user)
        return user_in_json

    @route('/admin/create-user')
    @cherrypy.tools.json_out()
    @authenticated
    def create_user(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_user = json.loads(rawbody)

        # Check username
        username_checking = self.check_username(json_user['username'])
        if not (username_checking is None):
            return username_checking
        salt = self.settings.cogenda_app.cogenda_salt
        user = User(
                json_user['username'], 
                hmac.new(salt, json_user['password']).hexdigest(),
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
    @authenticated
    def update_user(self):
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
        salt = self.settings.cogenda_app.cogenda_salt

        # Assemble user
        user = User(
                json_user['username'],
                hmac.new(salt, json_user['password']).hexdigest(),
                json_user['company'],
                json_user['email'],
                json_user['mobile'],
                json_user['role'],
                json_user['resource'],
                json_user['notes'],
                json_user['active'])
        user.updated_date = datetime.now()
        user = User.update_user(cherrypy.request.db, origin_user, user)
        return self.jsonify_model(user)

    @route('/admin/delete-user/:uid')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def destroy_user(self, uid):
        ids = uid.split(",")
        count = []
        for id in ids:
            count.append(User.delete_by_uid(cherrypy.request.db, id))
        return count

    @route('/admin/resources')
    @cherrypy.tools.json_out()
    @authenticated
    def resource_mgmt_data(self):
        all_resources = Resource.list(cherrypy.request.db)
        resources_in_json = []
        for resource in all_resources:
            resources_in_json.append(self.jsonify_model(resource))
        return resources_in_json


    @route('/admin/update-resource')
    @cherrypy.tools.json_out()
    @authenticated
    def update_resource(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_resource = json.loads(rawbody)

         # Get original user by id
        origin_resource = Resource.get_by_rid(cherrypy.request.db, json_resource['id'])

        # Assemble resource
        resource = Resource(
                json_resource['type'],
                json_resource['active'])
        resource = Resource.update_resource(cherrypy.request.db, origin_resource, resource)
        return self.jsonify_model(resource)


    @route('/api/modify-resource')
    @cherrypy.tools.json_out()
    def modify_resource(self):
        """ API for remote cloud sync service"""
        #if not self.user:
        #    return json.dumps({'success': False, 'msg': 'User can not authenticate!'})
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_resource = json.loads(rawbody)
        
        name = json_resource['filename']
        vendor = json_resource['server']
        status = json_resource['status']
        url = json_resource['url']
        type = json_resource['type']
        session = cherrypy.request.db
        try:
            resource = Resource.get_resource_by_name_vendor(session, name, vendor)
            if not resource:
                resource = Resource(name, type, vendor, url, status)
                session.add(resource)
            else:
                resource.name = name
                resource.vendor = vendor
                resource.status = status
                resource.url = url
                resource.type = type
                session.commit()
        except DBAPIError, err:
            return json.dumps({'success': False, 'msg': 'Sync resource failed!'})
        return json.dumps({'success': True, 'msg': 'Sync resource success!'})


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


    def check_username(self, username):
        user = User.get_by_username(cherrypy.request.db, username)
        if not (user is None):
            return  u"The username is existing."
