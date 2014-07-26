# -*- coding: utf-8 -*-

import unittest
from base_test_case import BaseCherryPyTestCase
import json, sys
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
        result = self.jsonify_response_body(response)
        self.assertTrue(result['success'], True)

    def test_destroy_resource_api(self):
        self._prepare_destroy_resource()
        """
        Test case for destroy resource API.
        """
        response = self.request('/api/destroy-resource', method='POST', data=self.payload_destroy, headers=self.headers_destroy) 
        self.assertEqual(response.output_status, '200 OK')
        result = self.jsonify_response_body(response)
        self.assertTrue(result['success'], True)

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


class AdminControllerTest(BaseCherryPyTestCase):

    """
    ADMIN CONTROLLER TEST CASES 
    TODO: 
    """
    def test_admin_login(self):
        self._login()
        response = self.request('/admin/login', method='POST', data=self.credentials, headers=self.authed_headers)
        self.assertEqual(response.output_status, '200 OK')

    """
    def test_admin_user_mgmt(self):
        # Before auth
        # response = self.request('/admin/user-mgmt', method='GET', headers=self.authed_headers)
        # self.assertEqual(response.output_status, '303 See Other')

        # After auth
        self._login()
        response = self.request('/admin/login', method='POST', data=self.credentials, headers=self.authed_headers)
        self.assertEqual(response.output_status, '200 OK')

        response = self.request('/admin/user-mgmt', method='GET', headers=self.authed_headers)
        self.assertEqual(response.output_status, '200 OK')
    """

    def _login(self):
        self.credentials = json.dumps({'json': {
            'username': 'admin',
            'password': 'admisn',
            'client': 'admin'}})
        auth_token = self._make_hamc_key(self.credentials)
        self.authed_headers = {'content-type': 'application/json', 'Authorization': auth_token}


class WebControllerTest(BaseCherryPyTestCase):
    
    """
    WEB CONTROLLER TEST CASES
    TODO:
    """
    @unittest.skip("unimplemented skipping")
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


def suite():
    suite_ws_controller = unittest.TestLoader().loadTestsFromTestCase(WSControllerTest)
    suite_auth_controller = unittest.TestLoader().loadTestsFromTestCase(AuthControllerTest)
    suite_admin_controller = unittest.TestLoader().loadTestsFromTestCase(AdminControllerTest)
    suite_web_controller = unittest.TestLoader().loadTestsFromTestCase(AdminControllerTest)
    return unittest.TestSuite([suite_ws_controller, suite_auth_controller, suite_admin_controller, suite_web_controller])


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
