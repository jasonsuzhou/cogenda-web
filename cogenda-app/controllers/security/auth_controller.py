# Controller to provide login and logout actions
from lib.controller import BaseController, route
import cherrypy
import hmac
from models import User
import json

class AuthController(BaseController):

    @route('/admin/login')
    def index(self):
        #cherrypy.tools.I18nTool.set_custom_language('en_US') 'zh_CN'
        return self.render_template('admin/security/login-user.html')


    @route('/security/authenticate')
    @cherrypy.tools.json_out(content_type='application/json')
    def authenticate(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_user = json.loads(rawbody)
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Auth User name :>>' + json_user['username']
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Auth Password :>>' + json_user['password']
        username = json_user['username']
        password = json_user['password']
        error_msg = self.check_credentials(username, password)
        if error_msg:
            resp = {'auth_success': False, 'msg': error_msg}
        else:
            cherrypy.session.regenerate()
            resp = {'auth_success': True, 'msg': u"User authenticated successfully."}
        return json.dumps(resp)


    @route('/security/logout')
    def logout(self):
        self.logoff()
        self.redirect('/admin/login')


    def check_credentials(self, username, password):
        user = User.get_by_username(cherrypy.request.db, username)
        """Verifies credentials for username and password."""
        if user is None or user.password != hmac.new('cogenda_salt', password).hexdigest():
            return u"Invalid user ID or password."
        self.login(user)