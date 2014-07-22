# -*- coding: utf-8 -*-

import unittest
from base_test_case import BaseCherryPyTestCase

import sys
sys.path.append('cogenda_app')
from cogenda_app import CogendaApp

class AdminControllerTest(BaseCherryPyTestCase):

    @classmethod
    def setUpClass(cls):
        cls.cogendaApp = CogendaApp('cogenda-test.ini')
        cls.cogendaApp.bootstrap() 

    @classmethod
    def tearDownClass(cls):
        cls.cogendaApp.stop()

    def test_admin_login(self):
        response = self.request('/admin/login')
        self.assertEqual(response.output_status, '200 OK')

if __name__ == '__main__':
    unittest.main()
