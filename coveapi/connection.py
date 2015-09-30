"""Module: `coveapi.connection`
Connection classes for accessing COVE API.
"""
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from coveapi import COVEAPI_HOST, COVEAPI_ENDPOINT_CATEGORIES, \
    COVEAPI_ENDPOINT_GROUPS, COVEAPI_ENDPOINT_PROGRAMS, \
    COVEAPI_ENDPOINT_VIDEOS, COVEAPI_ENDPOINT_GRAVEYARD
from coveapi.auth import PBSAuthorization


class COVEAPIConnection(object):
    """Connect to the COVE API service.

    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key
    `api_host` -- host of COVE API (default: COVEAPI_HOST)

    Returns:
    `coveapi.connection.COVEAPIConnection` instance
    """
    def __init__(self, api_app_id, api_app_secret, api_host=COVEAPI_HOST):
        self.api_app_id = api_app_id
        self.api_app_secret = api_app_secret
        self.api_host = api_host
        self.session = requests.Session()


    @property
    def programs(self, **params):
        """Handle program requests.

        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)

        Returns:
        `coveapi.connection.Requestor` instance
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_PROGRAMS)
        return Requestor(self.session, self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)


    @property
    def categories(self, **params):
        """Handle category requests.

        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)

        Returns:
        `coveapi.connection.Requestor` instance
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_CATEGORIES)
        return Requestor(self.session, self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)


    @property
    def groups(self, **params):
        """Handle group requests.

        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)

        Returns:
       `coveapi.connection.Requestor` instance
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_GROUPS)
        return Requestor(self.session, self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)


    @property
    def videos(self, **params):
        """Handle video requests.

        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)

        Returns:
        `coveapi.connection.Requestor` instance
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_VIDEOS)
        return Requestor(self.session, self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)

    @property
    def graveyard(self, **params):
        """Handle graveyard requests.

        Keyword arguments:
        `**params` -- deleted_since (see api documentation)

        Returns:
        `coveapi.connection.Requestor` instance
        """
        endpoint = '%s%s' % (self.api_host, COVEAPI_ENDPOINT_GRAVEYARD)
        return Requestor(self.session, self.api_app_id, self.api_app_secret, endpoint,
                         self.api_host)


class Requestor(object):
    """Handle API requests.

    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key
    `endpoint` -- endpoint of COVE API request

    Returns:
    `coveapi.connection.Requestor` instance
    """
    def __init__(self, session, api_app_id, api_app_secret, endpoint,
                 api_host=COVEAPI_HOST):
        self.api_app_id = api_app_id
        self.api_app_secret = api_app_secret
        self.endpoint = endpoint
        self.api_host = api_host
        self.session = session


    def get(self, resource, **params):
        """Fetch single resource from API service.

        Keyword arguments:
        `resource` -- resource id or uri
        `**params` -- filters, fields, sorts (see api documentation)

        Returns:
        `dict` (json)
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
        `dict` (json)
        """
        return self._make_request(self.endpoint, params)

    def deleted_since(self, **params):
        """Fetch deleted cove assets per 'deleted_since' parm.

        Keyword arguments:
        `**params` -- datetime (see api documentation)

        Returns:
        `dict` (json)
        """
        return self._make_request(self.endpoint, params)

    def _make_request(self, endpoint, params=None):
        """Send request to COVE API and return results as json object.

        Keyword arguments:
        `endpoint` -- endpoint of COVE API request
        `**params` -- filters, fields, sorts (see api documentation)

        Returns:
        `dict` (json)
        """
        if not params:
            params = {}

        query = endpoint
        if params:
            params = list(params.items())
            params.sort()

            # Note: We're using urlencode() below which escapes spaces as
            # a plus ("+") since that is what the COVE API expects. But a space
            # should really be encoded as "%20" (ie. urllib.quote()). I believe
            # this is a bug in the COVE API authentication scheme... but we have
            # to live with this in the client. We'll update this to use "%20"
            # once the COVE API supports it properly.
            query = '%s?%s' % (query, urlencode(params))

        req = requests.Request('GET', query)
        r = req.prepare()

        auth = PBSAuthorization(self.api_app_id, self.api_app_secret)
        signed_request = auth.sign_request(r)

        response = self.session.send(signed_request)

        return response.json()
