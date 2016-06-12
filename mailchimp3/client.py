from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import requests
import json
import logging

if True:
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 2

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig() 
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


class Mailchimp:
    """
    Mailchimp Client class 
    """
    def __init__(self):
        try:
            self.apikey = settings.MAILCHIMP_API_KEY
        except AttributeError, e:
            raise ImproperlyConfigured('You must provide a MAILCHIMP_API_KEY')

        parts = self.apikey.split('-')
        if len(parts) != 2:
            raise ImproperlyConfigured('Invalid MAILCHIMP_API_KEY ')
        
        self.shard = parts[1]
        print self.apikey
        self.api_root = "https://" + self.shard + ".api.mailchimp.com/3.0/"


    def request(self, resource, endpoint, method='GET',data={}, params={}):
        try:
            endpoint = urlparse.urljoin(self.api_root, endpoint)
            response = getattr(requests, method.lower())(endpoint,
                                                         auth=('apikey', self.apikey),
                                                         verify=False,
                                                         data=json.dumps(data),
                                                         params=params)
            
            response.raise_for_status()

            try:
                body = response.json() 
            except Exception, e:
                return None

            response = None
            print body
            try:
                response = body[resource]
            except KeyError, e:
                response = body

            return response
        except Exception, e:
            raise e

