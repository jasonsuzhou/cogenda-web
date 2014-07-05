#-*- coding:utf-8 -*-


from lib.controller import BaseController, route, authenticated
from datetime import datetime
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
import json
import hmac
import string
from random import choice

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


    """
    TODO: Need to combined load user data 
    """ 
    @route('/admin/init-user-table-title')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def init_user_table_title(self):
        username = _('User Name')
        company = _('Company')
        email = _('E-mail')
        mobile = _('Mobile')
        role = _('Role')
        active = _('Active')
        return json.dumps({'username': username,'company':company,'email':email,'mobile':mobile,'role':role,'active':active})


    """
    TODO: Need to combined to load resource data 
    """ 
    @route('/admin/init-resource-table-title')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def init_resource_table_title(self):
        resource_name = _('Resource Name')
        vendor = _('Vendor')
        url = _('URL')
        uploaded_date = _('Uploaded Date')
        type = _('Type')
        active = _('Active')
        description=_('Description')
        return json.dumps({'Resource Name': resource_name, 'Description':description, 'Vendor':vendor, 'URL':url, 'Uploaded Date':uploaded_date, 'Type':type, 'Active':active})


    @route('/admin/init-table-language')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def init_table_language(self):
        sProcessing = _('sProcessing')
        sShowRows = _('ShowRows')
        sZeroRecords = _('sZeroRecords')
        sInfo = _('sInfo')
        sInfoEmpty = _('sInfoEmpty')
        sInfoFiltered = _('sInfoFiltered')
        sInfoPostFix = _('sInfoPostFix')
        sSearch = _('sSearch')
        oPaginate_sFirst = _('oPaginate_sFirst')
        oPaginate_sPrevious = _('oPaginate_sPrevious')
        oPaginate_sNext = _('oPaginate_sNext')
        oPaginate_sLast = _('oPaginate_sLast')
        return json.dumps({'sProcessing': sProcessing,'sShowRows':sShowRows,'sZeroRecords':sZeroRecords,'sInfo':sInfo,'sInfoEmpty':sInfoEmpty,
                           'sInfoFiltered':sInfoFiltered,'sInfoPostFix':sInfoPostFix,'sSearch':sSearch,'oPaginate_sFirst':oPaginate_sFirst,
                           'oPaginate_sPrevious':oPaginate_sPrevious,'oPaginate_sNext':oPaginate_sNext,'oPaginate_sLast':oPaginate_sLast})



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

        for i in range(len(resources_in_json)):
            if i == len(resources_in_json):
                break
            resource = resources_in_json[i]
            if i != len(resources_in_json) - 1:
                next_resource = resources_in_json[i + 1]
                if resource['name'] == next_resource['name']:
                    resource['id'] = resource['id'] + ":" + next_resource['id']
                    resource['vendor'] = resource['vendor'] + "/" + next_resource['vendor']
                    resources_in_json.remove(next_resource)
        return resources_in_json


    @route('/admin/update-resource')
    @cherrypy.tools.json_out()
    @authenticated
    def update_resource(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_resource = json.loads(rawbody)

        ids = []
        resources_in_json = []
        if ":" in json_resource['id']:
            ids = json_resource['id'].split(":")
        else:
            ids.append(json_resource['id'])
        # Get resources by ids
        all_resources = Resource.get_by_rids(cherrypy.request.db, ids)
        for resource in all_resources:
            resource = Resource.update_resource(cherrypy.request.db, resource, json_resource['desc'], json_resource['type'], json_resource['active'])
            resources_in_json.append(self.jsonify_model(resource))
        return resources_in_json


    @route('/admin/fetch-resource/:rid')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def get_resource_by_id(self, rid):
        ids = []
        resources_in_json = []
        if ":" in rid:
            ids = rid.split(":")
        else:
            ids.append(rid)
        all_resources = Resource.get_by_rids(cherrypy.request.db, ids)
        for resource in all_resources:
            resources_in_json.append(self.jsonify_model(resource))
        return resources_in_json


    @route('/admin/reset-password')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def reset_password(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_request = json.loads(rawbody)
        name = json_request['username']
        receiver = json_request['email']
        sender = self.settings.mailer.smtp_user
        chars = string.letters + string.digits
        gen_pwd = ''.join(choice(chars) for _ in xrange(8))
        msg = 'Your password has been reset to: '+ gen_pwd + '.'
        try:
            self.send_mail('mail/req_account_tpl.html', 'Cogenda Support Team', name, sender, receiver, msg, 'Reset password')

            #Update user password here...
            origin_user = User.get_by_username(cherrypy.request.db, name)
            User.update_user_password(cherrypy.request.db, origin_user, gen_pwd)
        except Exception as err:
            print err
            log.error('Reset password operation error %s' % err)
            return json.dumps({'is_success': False, 'msg': 'Reset password failure!'})
        return json.dumps({'is_success': True, 'msg': 'Reset password successfully!'})


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
            elif col_name == 'id':
                json[col_name] = str(col_val)
            else:
                json[col_name] = col_val
        return json


    def check_username(self, username):
        user = User.get_by_username(cherrypy.request.db, username)
        if not (user is None):
            return  u"The username is existing."
