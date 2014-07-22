# -*- coding:utf-8 -*-

from lib.controller import BaseController, route, authenticated
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
from fuzzywuzzy import fuzz
from urlparse import urlparse
import os
import random
import json
from geoip import geolite2
from sqlalchemy.exc import DBAPIError
from lib import const

# Load logger
import logging
log = logging.getLogger(__name__)


class WebController(BaseController):
    """
    This WebController is used to provide api for frontend page
    """

    LAST_ARTICLE_FLAG = 'index'

    @route('/')
    def index(self):
        content = self.render_template('web/article/index.md')
        news = self.render_template('web/news/index.md')
        nav_infos = self._retrieve_nav_info()
        return self.render_template(
            'web/index.html',
            nav_infos=nav_infos,
            content=content,
            news=news,
            sidebar=self._retrieve_random_sidebar())

    @route('/article/:article_name')
    def serve_article(self, article_name):
        nav_infos = self._retrieve_nav_info()
        return self.render_template(
            'web/index.html',
            nav_infos=nav_infos,
            content=self._retrieve_optimized_article(article_name),
            news=self.render_template('web/news/index.md'),
            sidebar=self._retrieve_random_sidebar())

    @route('/check-resource/:rid')
    @cherrypy.tools.json_out(content_type='application/json')
    def check_resource(self, rid):
        log.debug("[Cogenda-web] - Check restricted resource: %s." % rid)
        try:
            resource = Resource.get_by_rid(cherrypy.request.db, rid)
        except DBAPIError, err:
            log.error('Database operation error %s' % err)
            return json.dumps({'msg': _('Encounter error in server')})

        # 4-AllUser - Software Packages, 5-AllUser - Installer, 6-Private
        if resource.type == const.RESOURCE_TYPE_ALLUSER_SOFTWARE_PACKAGES or \
                resource.type == const.RESOURCE_TYPE_ALLUSER_INSTALLER or \
                resource.type == const.RESOURCE_TYPE_PRIVATE:
            if self.user is None:
                return json.dumps({'auth_status': False, 'msg': _('This kind resource requires your login')})
        return json.dumps({'auth_status': True, 'link': '%s%s' % ('/download/', rid)})

    @route('/news/:news_name')
    def serve_news(self, news_name):
        pass

    @route('/switch/:locale')
    @cherrypy.tools.json_out(content_type='application/json')
    def switch_locale(self, locale):
        cherrypy.tools.I18nTool.set_custom_language(locale)
        cherrypy.tools.I18nTool.default = locale
        cherrypy.session['_lang_'] = locale
        refer = cherrypy.request.headers.get('Referer', '/')
        path = urlparse(refer).path
        if path.startswith('/article'):
            article_name = path.replace('/article/', '')
            self.LAST_ARTICLE_FLAG = article_name
        return json.dumps({'is_success': True, 'uri': self.LAST_ARTICLE_FLAG})

    @route('/web/init-common-language')
    @cherrypy.tools.json_out(content_type='application/json')
    def init_common_language(self):
        two_passwords_not_same = _('Two passwords are not the same')
        password_changed_successfully = _('Password is changed successfully')
        encounter_error_in_server = _('Encounter error in server')
        username = ''
        if self.user:
            username = self.user[0]
        return json.dumps({
            'username': username,
            'myprofile': _('My Profile'),
            'signout': _('Sign Out'),
            'Two passwords are not the same': two_passwords_not_same,
            'Password is changed successfully': password_changed_successfully,
            'Encounter error in server': encounter_error_in_server})

    @route('/download/:resource_id')
    def serve_downloads(self, resource_id):
        log.debug("[Cogenda-web] - Fetch db resource id: %s" % resource_id)
        try:
            resource = Resource.get_by_rid(cherrypy.request.db, resource_id)
        except DBAPIError, err:
            log.error('Database operation error %s' % err)
            return json.dumps({'msg': _('Encounter error in server')})
        if resource is None:
            return self.index()
        # 4,5-Installer, 6-Private
        if resource.type in (const.RESOURCE_TYPE_ALLUSER_SOFTWARE_PACKAGES, const.RESOURCE_TYPE_ALLUSER_INSTALLER, const.RESOURCE_TYPE_PRIVATE):
            if self.user is None:
                return self.index()
            elif resource.type == const.RESOURCE_TYPE_PRIVATE:
                # 6-Private
                resources_in_json = []
                self._auth_private_resource(resource, resources_in_json)
                if len(resources_in_json) == 0:
                    return self.index()
        cherrypy.response.headers["Content-Type"] = "application/octet-stream"
        cd = 'attachment; filename="%s"' % resource.name
        cherrypy.response.headers["Content-Disposition"] = cd
        resource_url_partial = resource.url.replace('http://', '').replace('https://', '')
        cherrypy.response.headers['X-Accel-Redirect'] = '/resource/%s' % (resource_url_partial)

    @route('/user/request-an-account')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json')
    def request_an_account(self):
        json_payload = cherrypy.request.json
        json_request = json_payload['json']
        name = json_request['username']
        sender = json_request['email']
        message = 'This mail is going to request an account, below is the note: <br/><br/> %s' % json_request['notes']
        log.debug("[Cogenda-web] - Request an account: %s,%s,%s" % (name, sender, message))
        try:
            self.send_mail('mail/mail_tpl.html', name, 'Support', self.settings.mailer.smtp_user, 'kkiiiu@gmail.com', message)
        except Exception as err:
            log.error('Send mail operation error %s' % err)
            return json.dumps({'is_success': False, 'msg': _('RequestMailSendFailure')})
        return json.dumps({'is_success': True, 'msg': _('RequestMailSendSuccessfully')})

    @route('/user/user-profile/:username')
    @cherrypy.tools.json_out()
    @authenticated
    def fetch_user_profile(self, username):
        log.debug("[Cogenda-web] - Fetch user profile: %s" % username)
        user = User.get_by_username(cherrypy.request.db, username)
        return user.jsonify

    @route('/user/change-password')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @authenticated
    def change_password(self):
        json_payload = cherrypy.request.json
        json_user = json_payload['json']
        log.debug("[Cogenda-web] - Change user password: %s" % json_user['username'])
        origin_user = User.get_by_username(cherrypy.request.db, json_user['username'])
        salt = self.settings.cogenda_app.cogenda_salt
        user = User.update_user_password(cherrypy.request.db, origin_user, json_user['password'], salt)
        return user.jsonify

    def _retrieve_nav_info(self):
        site_navs, sub_nav_captions = self._retrieve_menu_info()
        nav_infos = []
        for idx, (nav_name, nav_key) in enumerate(site_navs):
            link = '/'
            nav_key = nav_key.lower().strip()
            if nav_key != 'home':
                link = "%sarticle/%s" % (link, nav_key)
            sub_nav_caption = sub_nav_captions[idx]
            subnav_content = self.render_template('web/subnav/subnav-%s.md' % (nav_key), sub_nav_caption=sub_nav_caption)
            nav = (link, nav_name, subnav_content)
            nav_infos.append(nav)
        return nav_infos

    def _retrieve_random_sidebar(self):
        sidebar_files = self.context.sidebar_files.values()
        sidebar_choice = random.choice(sidebar_files)
        return self.render_template('web/sidebar/%s' % (sidebar_choice))

    def _retrieve_optimized_article(self, article_name):
        choice = self._optimize_assets(self.context.article_files, article_name)
        best_choice = 'web/article/%s' % (choice)
        # For download page
        if 'download' in choice:
            (
                private_resources,
                alluser_ins_resources,
                alluser_pac_resources,
                public_exp_resources,
                public_doc_resources,
                public_pub_resources) = self._fetch_resources()
            return self.render_template(
                best_choice,
                publications=public_pub_resources,
                documentations=public_doc_resources,
                examples=public_exp_resources,
                installers=alluser_ins_resources,
                software_packages=alluser_pac_resources,
                privates=private_resources)
        return self.render_template(best_choice)

    def _retrieve_optimized_news(self, news_name):
        choice = self._optimize_assets(self.context.news_files, news_name)
        best_choice = 'web/news/%s' % (choice)
        return self.render_template(best_choice)

    def _optimize_assets(self, asset_files, asset_name):
        best_choice = 'index.md'
        best_ratio = None
        for (key, val) in asset_files.items():
            asset = os.path.splitext(val)[0]
            ratio = fuzz.ratio(asset_name, asset)
            if not best_ratio:
                best_ratio = ratio
                best_choice = val
            if best_ratio < ratio:
                best_ratio = ratio
                best_choice = val
        return best_choice

    def _filter_resources_by_vendor(self, grouped_resources):
        """
        According vendor to filter out each type of resources
        """
        vendor = self._gen_vendor()
        public_exp_resources = []
        public_doc_resources = []
        public_pub_resources = []
        alluser_ins_resources = []
        alluser_pac_resources = []
        private_resources = []

        for tupled_resource in grouped_resources:
            this_resource = tupled_resource[0]
            that_resource = tupled_resource[1]
            _resource = this_resource
            if that_resource and that_resource.vendor == vendor:
                _resource = that_resource

            # Processing picked resource
            # 6-Private
            if _resource.type == const.RESOURCE_TYPE_PRIVATE and self.user:
                self._auth_private_resource(_resource, private_resources)
            # Other type resource: 1, 2, 3, 4, 5
            elif _resource.type == const.RESOURCE_TYPE_ALLUSER_INSTALLER:
                alluser_ins_resources.append(_resource.jsonify)
            elif _resource.type == const.RESOURCE_TYPE_ALLUSER_SOFTWARE_PACKAGES:
                alluser_pac_resources.append(_resource.jsonify)
            elif _resource.type == const.RESOURCE_TYPE_PUBLIC_EXAMPLES:
                public_exp_resources.append(_resource.jsonify)
            elif _resource.type == const.RESOURCE_TYPE_PUBLIC_DOCUMENTATION:
                public_doc_resources.append(_resource.jsonify)
            elif _resource.type == const.RESOURCE_TYPE_PUBLIC_PUBLICATIONS:
                public_pub_resources.append(_resource.jsonify)
        return private_resources, alluser_ins_resources, alluser_pac_resources, public_exp_resources, public_doc_resources, public_pub_resources

    def _gen_vendor(self):
        """
        Generate vendor by GeoIP.
        """
        remote_ip = cherrypy.request.remote.ip
        forwarded_ip = cherrypy.request.headers.get("X-Forwarded-For")
        match = geolite2.lookup(forwarded_ip or remote_ip)
        country_code = None
        if match:
            country_code = match.country
        log.info('[Cogenda-web] - Web client forwarded_ip >> [%s] remote_ip >> [%s] country_code >> [%s]' % (forwarded_ip, remote_ip, country_code))
        vendor = const.VENDOR_TYPE_S3
        if country_code and country_code == 'CN':
            vendor = const.VENDOR_TYPE_OOS
        log.info('[Cogenda-web] - load resource from vendor %s' % vendor)
        return vendor

    def _auth_private_resource(self, resource, resources_in_json):
        """
        Authenticate private resource for login user
        """
        restricted_res = '%s%s%s' % (',', self.user[3], ",")
        log.debug('[Cogenda-web] - User:%s, own resource:%s' % (self.user[0], restricted_res))
        log.debug('[Cogenda-web] - User requires resource:%s' % resource.id)
        # Resource
        if self.user[2] == const.USER_TYPE_RESOURCE:
            return
        # Resource Owner
        elif self.user[2] == const.USER_TYPE_RESOURCE_OWNER:
            p1 = '%s%s%s' % (',', str(resource.id), ",")
            p2 = '%s%s%s' % (':', str(resource.id), ",")
            p3 = '%s%s%s' % (',', str(resource.id), ":")
            if not(p1 in restricted_res) and not(p2 in restricted_res) and not(p3 in restricted_res):
                return
            resources_in_json.append(resource.jsonify)
        # Administrator
        elif self.user[2] == const.USER_TYPE_ADMINISTRATOR:
            resources_in_json.append(resource.jsonify)

    def _retrieve_menu_info(self):
        """
            Make navigation menu items and sub menu items.
        """
        SITE_MENU_ITEMS = [
            (_('Home'), 'home'),
            (_('Products'), 'products'),
            (_('Applications'), 'applications'),
            (_('Licensing'), 'licensing'),
            (_('Downloads'), 'downloads'),
            (_('Corporate'), 'corporate'),
            (_('Contact'), 'contact')
        ]
        SITE_SUB_MENU_CAPTIONS = [
            'Home sub nav caption',
            'Products sub nav caption',
            'Applications sub nav caption',
            'Licensing sub nav caption',
            'Downloads sub nav caption',
            'Corporate sub nav caption',
            'Contact sub nav caption'
        ]
        return SITE_MENU_ITEMS, SITE_SUB_MENU_CAPTIONS

    def _fetch_resources(self):
        log.debug("[Cogenda-web] - Fetch all resources.")
        resources = Resource.fetch_grouped_active_resources(cherrypy.request.db)
        return self._filter_resources_by_vendor(resources)
