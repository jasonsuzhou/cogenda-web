# -*- coding:utf-8 -*-

from lib.controller import BaseController, route, authenticated
from datetime import datetime
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
import json
import hmac
import string
from random import choice
from lib import const

# Load logger
import logging
log = logging.getLogger(__name__)


class AdminController(BaseController):
    """
    This AdminController is used to provide api for admin management
    """

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
        log.debug('[Cogenda-web] - Fetch all user.')
        all_users = User.list(cherrypy.request.db)
        users_in_json = []
        for user in all_users:
            users_in_json.append(user.jsonify)
        users_in_json.append(self._init_user_table_title())
        return users_in_json

    @route('/admin/fetch-user/:uid')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def get_user_by_id(self, uid):
        log.debug('[Cogenda-web] - Fetch user:%s' % uid)
        user = User.get_by_uid(cherrypy.request.db, uid)
        return user.jsonify

    @route('/admin/init-common-language')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def init_common_language(self):
        modify_user = _('Modify User')
        save = _('Save')
        create_user = _('Create User')
        select_one_user = _('Select one user')
        select_more_than_one_user = _('Selected more than one user')
        remove_user_successful = _('Remove user successful')
        you_cannot_delete_yourself = _('You cannot delete yourself')
        return json.dumps({'Save': save,
                           'Create User': create_user,
                           'Modify User': modify_user,
                           'Yes': _('Yes'), 'No': _('No'),
                           'Resource': _('Resource'),
                           'Resource Owner': _('Resource Owner'),
                           'Administrator': _('Administrator'),
                           'Filter String': _('Filter String'),
                           'Select one user': select_one_user,
                           'Selected more than one user': select_more_than_one_user,
                           'Remove user successful': remove_user_successful,
                           'You cannot delete yourself': you_cannot_delete_yourself})

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
        return json.dumps({'sProcessing': sProcessing,
                           'sShowRows': sShowRows,
                           'sZeroRecords': sZeroRecords,
                           'sInfo': sInfo,
                           'sInfoEmpty': sInfoEmpty,
                           'sInfoFiltered': sInfoFiltered,
                           'sInfoPostFix': sInfoPostFix,
                           'sSearch': sSearch,
                           'oPaginate_sFirst': oPaginate_sFirst,
                           'oPaginate_sPrevious': oPaginate_sPrevious,
                           'oPaginate_sNext': oPaginate_sNext,
                           'oPaginate_sLast': oPaginate_sLast})

    @route('/admin/create-user')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @authenticated
    def create_user(self):
        json_payload = cherrypy.request.json
        json_user = json_payload['json']
        log.debug('[Cogenda-web] - Create user:%s' % json_user['username'])

        # Check username
        username_checking = self._check_username(json_user['username'])
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
        cherrypy.request.db.add(user)
        return user.jsonify

    @route('/admin/update-user')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @authenticated
    def update_user(self):
        json_payload = cherrypy.request.json
        json_user = json_payload['json']
        log.debug('[Cogenda-web] - Update user:%s' % json_user['username'])

        # Get original user by id
        origin_user = User.get_by_uid(cherrypy.request.db, json_user['id'])

        # Check username
        if origin_user.username != json_user['username']:
            username_checking = self._check_username(json_user['username'])
            if not (username_checking is None):
                return username_checking
        salt = self.settings.cogenda_app.cogenda_salt
        user = User.update_user(cherrypy.request.db, origin_user, json_user, salt)
        return user.jsonify

    @route('/admin/delete-user/:uid')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def destroy_user(self, uid):
        log.debug('[Cogenda-web] - Delete users:%s' % uid)
        ids = uid.split(",")
        count = []
        for id in ids:
            count.append(User.delete_by_uid(cherrypy.request.db, id))
        return count

    @route('/admin/resources')
    @cherrypy.tools.json_out()
    @authenticated
    def resource_mgmt_data(self):
        log.debug('[Cogenda-web] - Fetch all resources.')
        resources = []
        grouped_resources = Resource.fetch_grouped_resources(cherrypy.request.db)
        for tupled_resource in grouped_resources:
            this_resource = tupled_resource[0]
            that_resource = tupled_resource[1]
            resource = this_resource.jsonify
            if that_resource:
                resource['id'] = '%s:%s' % (this_resource.id, that_resource.id)
                resource['vendor'] = '%s/%s' % (self._convert_vendor_name(this_resource.vendor),
                                                self._convert_vendor_name(that_resource.vendor))
            else:
                resource['id'] = this_resource.id
                resource['vendor'] = self._convert_vendor_name(this_resource.vendor)
            resources.append(resource)
        # Append table titles
        resources.append(self._init_resource_table_title())
        return resources

    @route('/admin/private-resources')
    @cherrypy.tools.json_out()
    @authenticated
    def fetch_private_resources(self):
        log.debug('[Cogenda-web] - Fetch all private resources.')
        resources = []
        grouped_resources = Resource.fetch_grouped_private_resources(cherrypy.request.db)
        for tupled_resource in grouped_resources:
            this_resource = tupled_resource[0]
            that_resource = tupled_resource[1]
            resource = this_resource.jsonify
            if that_resource:
                resource['id'] = '%s:%s' % (this_resource.id, that_resource.id)
                resource['vendor'] = '%s/%s' % (self._convert_vendor_name(this_resource.vendor),
                                                self._convert_vendor_name(that_resource.vendor))
            else:
                resource['id'] = this_resource.id
                resource['vendor'] = self._convert_vendor_name(this_resource.vendor)
            resources.append(resource)
        return resources

    @route('/admin/update-resource')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @authenticated
    def update_resource(self):
        json_payload = cherrypy.request.json
        json_resource = json_payload['json']

        log.debug('[Cogenda-web] - Update resource:%s' % json_resource['id'])

        ids = []
        resources_in_json = []
        if ":" in json_resource['id']:
            ids = json_resource['id'].split(":")
        else:
            ids.append(json_resource['id'])
        # Get resources by ids
        all_resources = Resource.get_by_rids(cherrypy.request.db, ids)
        for resource in all_resources:
            resource = Resource.update_resource(cherrypy.request.db, resource, json_resource)
            resources_in_json.append(resource.jsonify)
        return resources_in_json

    @route('/admin/fetch-resource/:rid')
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def get_resource_by_id(self, rid):
        log.debug('[Cogenda-web] - Fetch resource:%s' % rid)
        ids = []
        resources_in_json = []
        if ":" in rid:
            ids = rid.split(":")
        else:
            ids.append(rid)
        all_resources = Resource.get_by_rids(cherrypy.request.db, ids)
        for resource in all_resources:
            resources_in_json.append(resource.jsonify)
        return resources_in_json

    @route('/admin/reset-password')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    @authenticated
    def reset_password(self):
        json_payload = cherrypy.request.json
        json_request = json_payload['json']
        name = json_request['username']
        receiver = json_request['email']
        sender = self.settings.mailer.smtp_user
        chars = '%s%s' % (string.letters, string.digits)
        gen_pwd = ''.join(choice(chars) for _ in xrange(8))
        # TODO: Email template!!!
        msg = 'This email confirms that your password has been changed. <br/><br/>' \
              'To log on to the site, use the following password: ' + gen_pwd + '.  <br/><br/>' \
              'If you have any questions or encounter any problem logging in, pl. contact administrator.'
        log.debug('[Cogenda-web] - Reset password for user:%s' % name)
        try:
            self.send_mail('mail/mail_tpl.html', 'Cogenda Support Team',
                           name, sender, receiver, msg, 'Your password has been reset!')

            # Update user password here...
            origin_user = User.get_by_username(cherrypy.request.db, name)

            salt = self.settings.cogenda_app.cogenda_salt
            User.update_user_password(cherrypy.request.db, origin_user, gen_pwd, salt)
        except Exception as err:
            log.error('Reset password operation error %s' % err)
            return json.dumps({'is_success': False, 'msg': _('PasswordResetFailure')})
        return json.dumps({'is_success': True, 'msg': _('PasswordResetWorks')})

    def _check_username(self, username):
        log.debug('[Cogenda-web] - Check username:%s' % username)
        user = User.get_by_username(cherrypy.request.db, username)
        if user:
            return _('The username is existing')

    def _convert_vendor_name(self, vendor):
        if vendor == const.VENDOR_TYPE_OOS:
            return const.VENDOR_OOS_DISPLAY_NAME
        elif vendor == const.VENDOR_TYPE_S3:
            return const.VENDOR_S3_DISPLAY_NAME
        else:
            return vendor

    def _init_user_table_title(self):
        userTableTitle = {}
        userTableTitle['username'] = _('User Name')
        userTableTitle['company'] = _('Company')
        userTableTitle['email'] = _('E-mail')
        userTableTitle['mobile'] = _('Mobile')
        userTableTitle['role'] = _('Role')
        userTableTitle['active'] = _('Active')
        return userTableTitle

    def _init_resource_table_title(self):
        resourceTable = {}
        resourceTable['Resource Name'] = _('Resource Name')
        resourceTable['Description'] = _('Description')
        resourceTable['Vendor'] = _('Vendor')
        resourceTable['URL'] = _('URL')
        resourceTable['Uploaded Date'] = _('Uploaded Date')
        resourceTable['Type'] = _('Type')
        resourceTable['Active'] = _('Active')
        return resourceTable
