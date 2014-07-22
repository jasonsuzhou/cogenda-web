# -*- coding: utf-8 -*-

import sys
sys.path.append('cogenda_app')
from cogenda_app import CogendaApp
import unittest
from base_test_case import BaseCherryPyTestCase
import cherrypy

def setUpModule():
    cogendaApp = CogendaApp('cogenda-test.ini')
    cogendaApp.bootstrap() 
setup_module = setUpModule

def tearDownModule():
    cherrypy.engine.exit()
teardown_module = tearDownModule

class AdminModuleTest(BaseCherryPyTestCase):

    def test_admin_login(self):
        response = self.request('/admin/login')
        self.assertEqual(response.output_status, '200 OK')

    #def test_echo(self):
    #    response = self.request('/echo', msg="hey there")
    #    self.assertEqual(response.output_status, '200 OK')
    #    self.assertEqual(response.body, ["hey there"])

    #    response = self.request('/echo', method='POST', msg="back from the future")
    #    self.assertEqual(response.output_status, '200 OK')
    #    self.assertEqual(response.body, ["back from the future"])

if __name__ == '__main__':
    unittest.main()
