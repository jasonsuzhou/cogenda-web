# Controller to provide login and logout actions
from lib.controller import BaseController, route
import cherrypy
import hmac
from models import User
from lib.i18ntool import ugettext as _
import json
from lib import const

import logging
log = logging.getLogger(__name__)

"""
TODO: 
    - Add code comments 
"""

class AuthController(BaseController):

    @route('/admin/login')
    def index(self):
        return self.render_template('admin/security/login-user.html')


    @route('/security/init-common-language')
    @cherrypy.tools.json_out(content_type='application/json')
    def init_common_language(self):
        user_authenticated_successfully = _('User authenticated successfully')
        invalid_userid_or_password = _('Invalid user ID or password')
        you_have_insufficient_privileges = _('You have insufficient privileges')
        return json.dumps({'User authenticated successfully': user_authenticated_successfully,
                           'Invalid user ID or password': invalid_userid_or_password,
                           'You have insufficient privileges': you_have_insufficient_privileges})


    @route('/security/authenticate')
    @cherrypy.tools.json_out(content_type='application/json')
    def authenticate(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_user = json.loads(rawbody)
        username = json_user['username']
        password = json_user['password']
        client = json_user['client']
        refer = cherrypy.request.headers.get('Referer','/admin/user-mgmt')
        if refer.endswith('/admin/login'):
            refer = '/admin/user-mgmt'
        error_msg = self.check_credentials(username, password, client)
        if error_msg:
            resp = {'auth_success': False, 'msg': error_msg}
            log.debug('[Cogenda-web] - Auth failed msg: %s,%s,%s' %(username, password, error_msg))
        else:
            resp = {'auth_success': True, 'msg': _('User authenticated successfully'), 'refer': refer}
            log.debug('[Cogenda-web] - User %s login successfully.' % username)
        return json.dumps(resp)


    @route('/security/logout')
    def logout(self):
        self.logoff()
        self.redirect('/admin/login')


    @route('/web/logout')
    def web_logout(self):
        self.logoff()
        self.redirect('/')


    def check_credentials(self, username, password, client):
        user = User.get_by_username(cherrypy.request.db, username)
        """Verifies credentials for username and password."""
        salt = self.settings.cogenda_app.cogenda_salt
        if user is None or user.password != hmac.new(salt, password).hexdigest():
            return _('Invalid user ID or password')
        if not user.active:
            return _('This user is inactive')
        if client == const.CLIENT_TYPE_ADMIN and user.role != const.USER_TYPE_ADMINISTRATOR:
            return _('You have insufficient privileges')
        self.login(user, client)
