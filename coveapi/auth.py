"""Module: `coveapi.auth`
Authorization classes for signing COVE API requests.
"""
import hmac
from hashlib import sha1
import time
from base64 import urlsafe_b64encode
from os import urandom


class PBSAuthorization(object):
    """Authorization class for signing COVE API requests.

    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key

    Returns:
    `coveapi.auth.PBSAuthorization` instance
    """
    def __init__(self, api_app_id, api_app_secret):
        self.api_app_id = api_app_id
        self.api_app_secret = api_app_secret


    def sign_request(self, request):
        """Sign request per PBSAuth specifications.

        Keyword arguments:
        `request` -- instance of `urllib2.Request`

        Returns:
        instance of `urllib2.Request` (signed)
        """
        timestamp = str(time.time())
        nonce = urlsafe_b64encode(urandom(32)).decode().strip("=")

        to_be_signed = 'GET%s%s%s%s' % (request.url, timestamp,
                                        self.api_app_id, nonce)
        signature = hmac.new(self.api_app_secret.encode('utf-8'),
                             to_be_signed.encode('utf-8'),
                             sha1).hexdigest()

        headers = {'X-PBSAuth-Timestamp': timestamp,
                   'X-PBSAuth-Consumer-Key': self.api_app_id,
                   'X-PBSAuth-Signature': signature,
                   'X-PBSAuth-Nonce': nonce}
        request.headers = headers

        return request
