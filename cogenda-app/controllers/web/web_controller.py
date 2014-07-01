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


    @route('/news/:news_name')
    def serve_news(self, news_name):
        pass


    @route('/switch/:locale')
    def switch_locale(self, locale):
        cherrypy.tools.I18nTool.set_custom_language(locale)
        cherrypy.tools.I18nTool.default=locale
        refer = cherrypy.request.headers.get('Referer','/')
        path = urlparse(refer).path
        if path.startswith('/article'): 
            article_name = path.replace('/article/', '')
            self.LAST_ARTICLE_FLAG = article_name 
        return self.serve_article(self.LAST_ARTICLE_FLAG)


    @route('/download/:resource_id')
    def serve_downloads(self, resource_id):
        """TODO: web login verification """
        log.debug("Fetch db resource id: %s" % resource_id);
        resource = Resource.get_by_rid(cherrypy.request.db, resource_id)
        cherrypy.response.headers["Content-Type"] = "application/octet-stream"
        cd = 'attachment; filename="%s"' % resource.name
        cherrypy.response.headers["Content-Disposition"] = cd
        resource_url_partial = resource.url.replace('http://', '')
        cherrypy.response.headers['X-Accel-Redirect'] = '/media/%s' %(resource_url_partial)
        #cherrypy.response.headers['X-Accel-Redirect'] = '/media/cogenda-media.oss-cn-hangzhou.aliyuncs.com/media/123.png?Expires=1403359250&OSSAccessKeyId=DvSB6U5JdgjPj1Zr&Signature=vdtP0ldMD0yCskxmGcPxuF0oPuM%3D'


    @route('/user/request-an-account')
    @cherrypy.tools.json_out(content_type='application/json')
    def request_an_account(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        json_request = json.loads(rawbody)
        name = json_request['username']
        sender = json_request['email']
        message = json_request['notes']
        try:
            print "==================================="
            print name, sender, message
            print "==================================="
            self.send_mail('mail/req_account_tpl.html', name, self.settings.mailer.smtp_user, self.settings.mailer.smtp_user, message)
        except Exception as err:
            log.error('Send mail operation error %s' % err)
            return json.dumps({'is_success': False, 'msg': 'Request mail send failure with error: %s' %err})
        return json.dumps({'is_success': True, 'msg': 'Request mail send successfully!'})


    @route('/user/user-profile/:username')
    @cherrypy.tools.json_out()
    @authenticated
    def request_account(self, username):
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

        origin_user = User.get_by_username(cherrypy.request.db, json_user['username'])

        user = User.update_user_password(cherrypy.request.db, origin_user, json_user['password'])
        return self.jsonify_model(user)


    def _retrieve_nav_info(self):
        site_navs = self.settings.web.site_navs
        sub_nav_captions=self.settings.web.sub_nav_captions.split('|')
        nav_infos=[]
        for idx, nav_name in enumerate(site_navs.split('|')):
            link = '/'
            if nav_name.lower().strip() != 'home':
               link = "%sarticle/%s" %(link, nav_name.lower().strip())
            caption = _(nav_name)
            sub_nav_caption = sub_nav_captions[idx]
            print sub_nav_caption
            subnav_content=self.render_template('web/subnav/subnav-%s.md' %(nav_name.lower()), sub_nav_caption=sub_nav_caption)
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
           asset= os.path.splitext(val)[0] 
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
            if col_name == 'created_date' or col_name == 'updated_date':
                continue
            else:
                json[col_name] = col_val
        return json

