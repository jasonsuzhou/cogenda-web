# Controller to provide login and logout actions
from lib.controller import BaseController, route
import cherrypy
import hmac
from models import User
import json

class AuthController(BaseController):

    @route('/admin/login')
    def index(self):
        return self.render_template('admin/security/login-user.html')


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
        else:
            resp = {'auth_success': True, 'msg': u"User authenticated successfully.", 'refer': refer}
        return json.dumps(resp)


    @route('/security/logout')
    def logout(self):
        self.logoff()
        self.redirect('/admin/login')


    def check_credentials(self, username, password, client):
        user = User.get_by_username(cherrypy.request.db, username)
        """Verifies credentials for username and password."""
        salt = self.settings.cogenda_app.cogenda_salt
        if user is None or user.password != hmac.new(salt, password).hexdigest():
            return u"Invalid user ID or password."
        if client == 'admin' and user.role != '3':
            return u"You have insufficient privileges."
        self.login(user, client)
