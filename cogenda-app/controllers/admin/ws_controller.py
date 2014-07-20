# -*- coding:utf-8 -*-

from lib.controller import BaseController, route
import cherrypy
import json
from models import Resource
from sqlalchemy.exc import DBAPIError

# Load logger
import logging
log = logging.getLogger(__name__)


class WSController(BaseController):

    """
    Webservice API for Cloud Sync service
    - Cloud Sync service will Create/Update/Destroy resources automatically.
    - Use HMAC to do webservice authtentication.
    """

    @route('/api/modify-resource')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def modify_resource(self):
        """ API for remote cloud sync service to create ro update resource """
        """ Create or update resources """
        json_payload = cherrypy.request.json
        if not self._verify_auth_token(json.dumps(json_payload)):
            return json.dumps({'success': False, 'msg': 'User operation not authorized!'})

        payload = json_payload['json']
        name = payload['filename']
        vendor = payload['server']
        url = payload['url']
        type = payload['type']
        desc = payload['desc']
        session = cherrypy.request.db
        try:
            resource = Resource.get_resource_by_name_vendor(session, name, vendor)
            if not resource:
                resource = Resource(name, desc, type, vendor, url)
                session.add(resource)
            else:
                resource.name = name
                resource.vendor = vendor
                resource.url = url
                resource.type = type
                resource.description = desc
                session.commit()
        except DBAPIError, err:
            log.error('Database operation error %s' % err)
            return json.dumps({'success': False, 'msg': 'Sync resource failed!'})
        return json.dumps({'success': True, 'msg': 'Sync resource success!'})

    @route('/api/destroy-resource')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def destory_resource(self):
        """ API for cloud sync service to destroy resource """
        json_payload = cherrypy.request.json
        if not self._verify_auth_token(json.dumps(json_payload)):
            return json.dumps({'success': False, 'msg': 'User operation not authorized!'})

        #payload = json.loads(rawbody)
        payload = json_payload['json']
        filename = payload['filename']
        vendor = payload['server']
        if not filename or not vendor:
            return json.dumps({'success': False, 'msg': 'Invalid request parameters!'})
        try:
            Resource.delete_resource_by_name_vendor(cherrypy.request.db, filename, vendor)
        except DBAPIError, err:
            log.error('Database operation error %s' % err)
            return json.dumps({'success': False, 'msg': 'Destory resource failed!'})
        return json.dumps({'success': True, 'msg': 'Destroy resource success!'})

    def _verify_auth_token(self, message):
        """ Verify auth token """
        client_auth_token = cherrypy.request.headers['Authorization']
        auth_token = self.make_auth_token(message)
        if not client_auth_token and client_auth_token != auth_token:
            return False
        return True
