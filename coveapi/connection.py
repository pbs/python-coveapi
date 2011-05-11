"""Module: `coveapi.connection`
Connection object for accessing COVE API.
"""
import hmac
import hashlib
import time
import urllib
import urllib2
from base64 import urlsafe_b64encode
from os import urandom

import simplejson as json

from coveapi import COVEAPI_HOST, COVEAPI_ENDPOINT_CATEGORIES, \
    COVEAPI_ENDPOINT_GROUPS, COVEAPI_ENDPOINT_PROGRAMS, \
    COVEAPI_ENDPOINT_VIDEOS
   

class COVEAPIConnection(object):
    """Connect to the COVE API service.

    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key
    `api_host` -- host of COVE API (default: COVEAPI_HOST)
    
    Returns:
    `coveapi.connection.COVEAPIConnection` object
    """
    def __init__(self, api_app_id, api_app_secret, api_host=COVEAPI_HOST):
        self.api_app_id = api_app_id
        self.api_app_secret = api_app_secret
        self.api_host = api_host


    @property
    def programs(self, **params):
        """Handle program requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `coveapi.connection.Requestor` object
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_PROGRAMS)
        return Requestor(self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)

    
    @property
    def categories(self, **params):
        """Handle category requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `coveapi.connection.Requestor` object
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_CATEGORIES)
        return Requestor(self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)

    
    @property
    def groups(self, **params):
        """Handle group requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
       `coveapi.connection.Requestor` object
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_GROUPS)
        return Requestor(self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)

        
    @property
    def videos(self, **params):
        """Handle video requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `coveapi.connection.Requestor` object
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_VIDEOS)
        return Requestor(self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)


class Requestor(object):
    """Handle API requests.
    
    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key
    `endpoint` -- endpoint of COVE API request
    
    Returns:
    `coveapi.connection.Requestor` object
    """
    def __init__(self, api_app_id, api_app_secret, endpoint,
                 api_host=COVEAPI_HOST):
        self.api_app_id = api_app_id
        self.api_app_secret = api_app_secret
        self.endpoint = endpoint
        self.api_host = api_host


    def get(self, resource, **params):
        """Fetch single resource from API service.

        Keyword arguments:
        `resource` -- resource id or uri
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `dict` json object
        """
        if type(resource) == int:
            endpoint = '%s%s/' % (self.endpoint, resource)
        else:
            if resource.startswith('http://'):
                endpoint = resource
            else:
                endpoint = '%s%s' % (self.api_host, resource)
        
        return self._make_request(endpoint, params)


    def filter(self, **params):
        """Fetch resources from API service per specified parameters.

        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `dict` json object
        """
        return self._make_request(self.endpoint, params)


    def _make_request(self, endpoint, params=None):
        """Send request to COVE API and return results as json object."""
        if not params:
            params = {}

        timestamp = str(time.time())
        nonce = urlsafe_b64encode(urandom(32)).strip("=")
        
        query = endpoint
        if params:
            params = params.items()
            params.sort()
            query = '%s?%s' % (query, urllib.urlencode(params))
            
        to_be_signed = 'GET%s%s%s%s' % (query, timestamp,
                                        self.api_app_id, nonce)
        signature = hmac.new(self.api_app_secret.encode('utf-8'),
                             to_be_signed.encode('utf-8'),
                             hashlib.sha1).hexdigest()
        headers = {
            'X-PBSAuth-Timestamp': timestamp,
            'X-PBSAuth-Consumer-Key': self.api_app_id,
            'X-PBSAuth-Signature': signature,
            'X-PBSAuth-Nonce': nonce
        }

        request = urllib2.Request(query, None, headers)
        response = urllib2.urlopen(request)
        
        return json.loads(response.read())
