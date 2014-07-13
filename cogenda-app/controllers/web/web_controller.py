#-*- coding:utf-8 -*-

from lib.controller import BaseController, route, authenticated
from datetime import datetime
from models import User, Resource
import cherrypy
from lib.i18ntool import ugettext as _
from datetime import datetime
from fuzzywuzzy import fuzz
from urlparse import urlparse
import logging 
import os
import random
import json
from geoip import geolite2
from sqlalchemy.exc import DBAPIError

log = logging.getLogger(__name__)

class WebController(BaseController):

    LAST_ARTICLE_FLAG='index'

    @route('/')
    def index(self):
        content = self.render_template('web/article/index.md')
        news = self.render_template('web/news/index.md')
        nav_infos = self._retrieve_nav_info()
        return self.render_template('web/index.html', 
                nav_infos=nav_infos,
                content=content, 
                news=news, 
                sidebar=self._retrieve_random_sidebar())


    @route('/article/:article_name')
    def serve_article(self, article_name):
        nav_infos = self._retrieve_nav_info()
        return self.render_template('web/index.html', 
                nav_infos=nav_infos,
                content=self._retrieve_optimized_article(article_name), 
                news=self.render_template('web/news/index.md'), 
                sidebar=self._retrieve_random_sidebar())


    @route('/resources')
    @cherrypy.tools.json_out()
    def load_resource(self):
        log.debug("[Cogenda-web] - Fetch all resources.")
        all_resources = Resource.list_active_resources(cherrypy.request.db)
        return self.filter_resources_by_vendor(all_resources)


    @route('/private-resources')
    @cherrypy.tools.json_out()
    def load_private_resource(self):
        log.debug("[Cogenda-web] - Fetch private resources.")
        private_resources = Resource.list_resource_by_type(cherrypy.request.db, '6')
        return self.filter_resources_by_vendor(private_resources)


    @route('/check-resource/:rid')
    @cherrypy.tools.json_out(content_type='application/json')
    def check_resource(self, rid):
        log.debug("[Cogenda-web] - Check restricted resource: %s." %rid)
        try:
            resource = Resource.get_by_rid(cherrypy.request.db, rid)
        except DBAPIError, err:
            log.error('Database operation error %s' % err)
            return json.dumps({'msg': _('Encounter error in server')})

        # 4-AllUser - Software Packages, 5-AllUser - Installer, 6-Private
        if resource.type == '4' or resource.type == '5' or resource.type == '6':
            if self.user is None:
                return json.dumps({'auth_status': False, 'msg': _('This kind resource requires your login')})
            else:
                return json.dumps({'auth_status': True, 'link': '/download/'+rid})
        return json.dumps({'auth_status': True, 'link': '/download/'+rid})


    @route('/news/:news_name')
    def serve_news(self, news_name):
        pass


    @route('/switch/:locale')
    @cherrypy.tools.json_out(content_type='application/json')
    def switch_locale(self, locale):
        cherrypy.tools.I18nTool.set_custom_language(locale)
        cherrypy.tools.I18nTool.default=locale
        cherrypy.session['_lang_'] = locale
        refer = cherrypy.request.headers.get('Referer','/')
        path = urlparse(refer).path
        if path.startswith('/article'): 
            article_name = path.replace('/article/', '')
            self.LAST_ARTICLE_FLAG = article_name 
        return json.dumps({'is_success': True, 'uri':self.LAST_ARTICLE_FLAG})


    @route('/web/init-common-language')
    @cherrypy.tools.json_out(content_type='application/json')
    def init_common_language(self):
        two_passwords_not_same = _('Two passwords are not the same')
        password_changed_successfully = _('Password is changed successfully')
        encounter_error_in_server = _('Encounter error in server')
        if self.user:
            username = self.user[0]
        else:
            username = ''
        return json.dumps({'username' : username, 'myprofile':_('My Profile'), 'signout': _('Sign Out'),
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
        cherrypy.response.headers["Content-Type"] = "application/octet-stream"
        cd = 'attachment; filename="%s"' % resource.name
        cherrypy.response.headers["Content-Disposition"] = cd
        resource_url_partial = resource.url.replace('http://', '').replace('https://', '')
        cherrypy.response.headers['X-Accel-Redirect'] = '/resource/%s' %(resource_url_partial)
        #cherrypy.response.headers['X-Accel-Redirect'] = '/resource/cogenda-media.oss-cn-hangzhou.aliyuncs.com/media/123.png?Expires=1403359250&OSSAccessKeyId=DvSB6U5JdgjPj1Zr&Signature=vdtP0ldMD0yCskxmGcPxuF0oPuM%3D'


    @route('/user/request-an-account')
    @cherrypy.tools.json_out(content_type='application/json')
    def request_an_account(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_request = json.loads(rawbody)
        name = json_request['username']
        sender = json_request['email']
        message = json_request['notes']
        log.debug("[Cogenda-web] - Request an account: %s,%s,%s" %(name, sender, message))
        try:
            self.send_mail('mail/req_account_tpl.html', name, 'Support', self.settings.mailer.smtp_user, 'kkiiiu@gmail.com', message)
        except Exception as err:
            log.error('Send mail operation error %s' % err)
            return json.dumps({'is_success': False, 'msg': 'Request mail send failure with error: %s' %err})
        return json.dumps({'is_success': True, 'msg': _('Request mail send successfully')})


    @route('/user/user-profile/:username')
    @cherrypy.tools.json_out()
    @authenticated
    def fetch_user_profile(self, username):
        log.debug("[Cogenda-web] - Fetch user profile: %s" %username)
        user = User.get_by_username(cherrypy.request.db, username)
        user_in_json = self.jsonify_model(user)
        return user_in_json


    @route('/user/change-password')
    @cherrypy.tools.json_out()
    @authenticated
    def change_password(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_user = json.loads(rawbody)
        log.debug("[Cogenda-web] - Change user password: %s" %json_user['username'])
        origin_user = User.get_by_username(cherrypy.request.db, json_user['username'])
        user = User.update_user_password(cherrypy.request.db, origin_user, json_user['password'])
        return self.jsonify_model(user)


    def _retrieve_nav_info(self):
        site_navs = self.settings.web.site_navs
        sub_nav_captions = self.settings.web.sub_nav_captions.split('|')
        nav_infos = []
        for idx, nav_name in enumerate(site_navs.split('|')):
            link = '/'
            if nav_name.lower().strip() != 'home':
               link = "%sarticle/%s" %(link, nav_name.lower().strip())
            caption = _(nav_name)
            sub_nav_caption = sub_nav_captions[idx]
            subnav_content = self.render_template('web/subnav/subnav-%s.md' %(nav_name.lower()), sub_nav_caption=sub_nav_caption)
            nav = (link, caption, subnav_content)
            nav_infos.append(nav)
        return nav_infos

    def _retrieve_random_sidebar(self):
        sidebar_files = self.context.sidebar_files.values()
        sidebar_choice = random.choice(sidebar_files)
        return self.render_template('web/sidebar/%s' %(sidebar_choice))


    def _retrieve_optimized_article(self, article_name):
        choice = self._optimize_assets(self.context.article_files, article_name)
        best_choice = 'web/article/%s' %(choice)
        return self.render_template(best_choice)


    def _retrieve_optimized_news(self, news_name):
        choice = self._optimize_assets(self.context.news_files, news_name)
        best_choice = 'web/news/%s' %(choice)
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


    def jsonify_model(self, model):
        """ Returns a JSON representation of an SQLAlchemy-backed object.
        """
        json = {}
        columns = model._sa_class_manager.mapper.mapped_table.columns
        for col in columns:
            col_name = col.name
            col_val = getattr(model, col_name)
            if col_name == 'created_date' or col_name == 'updated_date' or col_name == 'uploaded_date':
                continue
            else:
                json[col_name] = col_val
        return json

    def auth_private_resource(self, resource, resources_in_json):
        restricted_res = "," + self.user[3] + ","
        log.debug('[Cogenda-web] - User:%s, own resource:%s' %(self.user[0], restricted_res))
        log.debug('[Cogenda-web] - User requires resource:%s' %resource.id)
        # Resource
        if self.user[2] == '1':
            return
        # Resource Owner
        elif self.user[2] == '2':
            p1 = "," + str(resource.id) + ","
            p2 = ":" + str(resource.id) + ","
            p3 = "," + str(resource.id) + ":"
            if not(p1 in restricted_res) and not(p2 in restricted_res) and not(p3 in restricted_res):
                return
            else:
                resources_in_json.append(self.jsonify_model(resource))
        # Administrator
        elif self.user[2] == '3':
            resources_in_json.append(self.jsonify_model(resource))

    def gen_vendor(self):
        remote_ip = cherrypy.request.remote.ip
        forwarded_ip = cherrypy.request.headers.get("X-Forwarded-For")
        match = geolite2.lookup(forwarded_ip or remote_ip)
        country_code = None
        if match:
            country_code = match.country
            log.info('web client forwarded_ip >> [%s] remote_ip >> [%s] country_code >> [%s]' %(forwarded_ip, remote_ip, country_code))
        vendor = 'oss'
        if country_code and country_code == 'CN':
            log.info('load resource from vendor AliYun OSS')
            vendor = 'oss'
        else:
            log.info('load resource from vendor AWS S3.')
            vendor = 's3'
        return vendor

    def filter_resources_by_vendor(self, all_resources):
        vendar = self.gen_vendor()
        resources_in_json = []
        for i in range(len(all_resources)):
            if i == len(all_resources):
                break
            _resource = resource = all_resources[i]
            if i != len(all_resources) - 1:
                next_resource = all_resources[i + 1]
                if resource.name == next_resource.name:
                    if resource.vendor != vendar:
                        _resource = next_resource
                        all_resources.remove(resource)
                    else:
                        all_resources.remove(next_resource)
            # Processing picked resource
            # 6-Private
            if _resource.type == '6':
                if self.user:
                    self.auth_private_resource(_resource, resources_in_json)
                else:
                    continue
            # Other type resource: 1, 2, 3, 4, 5
            else:
                resources_in_json.append(self.jsonify_model(_resource))
        return resources_in_json
