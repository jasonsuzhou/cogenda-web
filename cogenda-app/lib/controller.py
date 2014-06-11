#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from os.path import split, abspath, join, dirname

import cherrypy
from cherrypy import thread_data

from cache import Cache
from jinja2 import Environment, FileSystemLoader, PackageLoader, ChoiceLoader
from babel.support import Translations
from i18ntool import I18nTool

import logging 
log = logging.getLogger(__name__)

#Initialization of I18nTool
cherrypy.tools.I18nTool = I18nTool(os.path.abspath( __file__ ))

__CONTROLLERS__ = []
__CONTROLLERSDICT__ = {}

def route(route, name=None, priority=50):
    def dec(func):
        actual_name = func.__name__
        if name:
            actual_name = name
        conf = (
            actual_name, {
                'route': route,
                'method': func.__name__,
                'priority': priority
            }
        )

        return func, conf

    return dec


def authenticated(func):
    def actual(*arguments, **kw):
        instance = arguments[0]
        user = instance.user
        if user:
            return func(*arguments, **kw)
        #else:
            #TODO: redirect to 401 page.

    actual.__name__ = func.__name__
    actual.__doc__ = func.__doc__
    return actual


class MetaController(type):
    def __init__(cls, name, bases, attrs):
        if 'BaseController' in globals() and \
                        issubclass(cls, globals()['BaseController']):
            __CONTROLLERS__.append(cls)
            __CONTROLLERSDICT__[name] = cls
            cls.__routes__ = []

            routes = []

            for attr, value in attrs.items():
                if isinstance(value, tuple) and len(value) is 2:
                    method, conf = value
                    routes.append((attr, method, conf, conf[1]['priority']))

            routes = sorted(routes, lambda i1, i2: cmp(i2[3], i1[3]))

            for attr, method, conf, priority in routes:
                setattr(cls, attr, method)
                cls.__routes__.append(conf)

        super(MetaController, cls).__init__(name, bases, attrs)

class BaseController(object):
    __metaclass__ = MetaController
    __routes__ = None

    def __init__(self, server=None):
        self.server = server

    def log(self, message):
        if self.settings.cogenda_app.as_bool('verbose'):
            cherrypy.log(message, "[%s]" % self.__class__.__name__)

    @classmethod
    def all(self):
        return __CONTROLLERS__

    @property
    def cache(self):
        return self.server.cache

    @property
    def settings(self):
        if not self.server:
            return None
        return self.server.context.settings

    @property
    def context(self):
        if not self.server:
            return None
        return self.server.context

    @property
    def name(self):
        return self.__class__.__name__.lower().replace("controller", "")

    @property
    def user(self):
        try:
            return cherrypy.session.get('authenticated_user', None)
        except AttributeError:
            return None

    def login(self, user):
        cherrypy.session['authenticated_user'] = user

    def logoff(self):
        cherrypy.session['authenticated_user'] = None

    def register_routes(self, dispatcher):
        for route in self.__routes__:
            route_name = "%s_%s" % (self.name, route[0])
            dispatcher.connect(route_name, route[1]["route"], controller=self, action=route[1]["method"])


    def render_template(self, template_file, **kw):
        """ Integrate with Jinja2 & Babel"""
        app_name = self.settings.cogenda_app.app_name
        mo_dir = os.path.join(os.path.abspath(os.curdir), app_name ,'i18n')
        if self.settings.cogenda_app.as_bool('daemon'):
            mo_dir = self.settings.cogenda_app.app_home + mo_dir
        log.debug(mo_dir)
        locale = str(cherrypy.response.i18n.locale)
        translations = Translations.load(mo_dir, locale, app_name)
        env = Environment(loader = PackageLoader(app_name, 'templates'), extensions=['jinja2.ext.i18n'])
        env.install_gettext_translations(translations)
        cherrypy.tools.jinja2env = env 
        template = cherrypy.tools.jinja2env.get_template(template_file)
        return template.render(user=self.user, settings=self.settings, **kw)


    def redirect(self, url):
        raise cherrypy.HTTPRedirect(url)

    def healthcheck(self):
        healthcheck_text = self.settings.cogenda_app.healthcheck_text
        return healthcheck_text or "WORKING"

