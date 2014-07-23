# -*- coding: utf-8 -*-

import unittest
from base_test_case import BaseCherryPyTestCase
import os, json, hmac, base64, hashlib, sys
sys.path.append('cogenda_app')
from cogenda_app import CogendaApp
import cherrypy

def setUpModule():
    cogendaApp = CogendaApp('cogenda-test.ini')
    cogendaApp.bootstrap() 

def tearDownModule():
    cherrypy.engine.exit()
    cherrypy.server.httpserver = None

class WSControllerTest(BaseCherryPyTestCase):

    """
    WS CONTROLLER TEST CASES
    """
    def test_modify_resource_api(self):
        self._prepare_modify_resource()
        """ 
        Test case for create or update resource API.
        """
        response = self.request('/api/modify-resource', method='POST', data=self.payload_modify, headers=self.headers_modify) 
        self.assertEqual(response.output_status, '200 OK')
        json_body = json.loads(response.body[0])
        print json_body
        #self.assertEqual(json_body[0], True)

    def test_destroy_resource_api(self):
        self._prepare_destroy_resource()
        """
        Test case for destroy resource API.
        """
        response = self.request('/api/destroy-resource', method='POST', data=self.payload_destroy, headers=self.headers_destroy) 
        self.assertEqual(response.output_status, '200 OK')
        json_body = json.loads(response.body[0])
        print json_body

    def _prepare_modify_resource(self):
        self.payload_modify = json.dumps({'json': {
            'filename': 'test_file',
            'url': 'http://localhost/test_url',
            'server': 'oss',
            'type': 1,
            'desc': 'cogenda unittest case.'
            }})
        auth_token_modify = self._make_hamc_key(self.payload_modify)
        self.headers_modify = {'content-type': 'application/json', 'Authorization': auth_token_modify}

    def _prepare_destroy_resource(self):
        self.payload_destroy = json.dumps({'json': {'filename': 'test_fle', 'server': 'oss'}})
        auth_token_destroy = self._make_hamc_key(self.payload_destroy)
        self.headers_destroy = {'content-type': 'application/json', 'Authorization': auth_token_destroy}

    def _make_hamc_key(self, message):
        """ Generate HMAC key """
        shared_secret = os.environ.get('COGENDA_SHARED_SECRET', 'cogenda-ws-secret')
        auth_token = base64.b64encode(hmac.new(shared_secret, message, digestmod=hashlib.sha256).digest())
        return auth_token 

class AdminControllerTest(BaseCherryPyTestCase):

    """
    ADMIN CONTROLLER TEST CASES 
    TODO: 
    """
    def test_admin_user_mgmt(self):
        pass

class WebControllerTest(BaseCherryPyTestCase):
    
    """
    WEB CONTROLLER TEST CASES
    TODO:
    """
    def test_web_login(self):
        pass

class AuthControllerTest(BaseCherryPyTestCase):

    """
    AUTH CONTROLLER TEST CASES
    TODO:
    """
    def test_admin_login(self):
        response = self.request('/admin/login')
        self.assertEqual(response.output_status, '200 OK')

if __name__ == '__main__':
    unittest.main()
