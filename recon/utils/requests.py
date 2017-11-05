import json
import requests
import socket
import ssl
import xml.etree.ElementTree

# create a global ssl context that ignores certificate validation
if hasattr(ssl, '_create_unverified_context'): 
    ssl._create_default_https_context = ssl._create_unverified_context

def encode_payload(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

class Request(object):

    def __init__(self, **kwargs):
        '''Initializes control parameters as class attributes.'''
        self.user_agent = requests.utils.default_user_agent() if 'user_agent' not in kwargs else kwargs['user_agent']
        self.debug = False if 'debug' not in kwargs else kwargs['debug']
        self.proxy = None if 'proxy' not in kwargs else kwargs['proxy']
        self.timeout = None if 'timeout' not in kwargs else kwargs['timeout']
        self.redirect = True if 'redirect' not in kwargs else kwargs['redirect']

    def send(self, url, method='GET', payload=None, headers=None, cookiejar=None, auth=None, content=''):
        '''Makes a web request and returns a response object.'''
        if method.upper() != 'POST' and content:
            raise RequestException('Invalid content type for the %s method: %s' % (method, content))
        # prime local mutable variables to prevent persistence
        if payload is None: payload = {}
        if headers is None: headers = {}
        if auth is None: auth = ()

        # set request arguments
        # process user-agent header
        headers['User-Agent'] = self.user_agent
        # process payload
        if content.upper() == 'JSON':
            headers['Content-Type'] = 'application/json'

        # process socket timeout
        if self.timeout:
            socket.setdefaulttimeout(self.timeout)
        
        # set handlers
        # declare handlers list according to debug setting
        # handlers = [urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPSHandler(debuglevel=1)] if self.debug else []

        # process proxies and add handler
        proxies = None
        if self.proxy:
            proxies = {'http': self.proxy, 'https': self.proxy}

        # install opener
        # opener = urllib2.build_opener(*handlers)
        # urllib2.install_opener(opener)

        # process method and make request
        try:
            if method == 'GET':
                resp = requests.get(url, params=payload, headers=headers, cookies=cookiejar, auth=auth, allow_redirects=self.redirect, proxies=proxies)
            elif method == 'POST':
                resp = requests.post(url, data=payload, headers=headers, cookies=cookiejar, auth=auth, allow_redirects=self.redirect, proxies=proxies)
            elif method == 'HEAD':
                resp = requests.head(url, params=payload, headers=headers, cookies=cookiejar, auth=auth, allow_redirects=self.redirect, proxies=proxies)
            else:
                raise RequestException('Request method \'%s\' is not a supported method.' % (method))
        except requests.exceptions.HTTPError as e:
            resp = e

        # build and return response object
        return ResponseObject(resp, cookiejar)

# class NoRedirectHandler(urllib2.HTTPRedirectHandler):

#     def http_error_302(self, req, fp, code, msg, headers):
#         pass

#     http_error_301 = http_error_303 = http_error_307 = http_error_302



class ResponseObject(object):

    def __init__(self, resp, cookiejar):
        # set raw response property
        self.raw = resp
        # set inherited properties
        self.url = resp.geturl()
        self.status_code = resp.getcode()
        self.headers = resp.headers.dict
        # detect and set encoding property
        self.encoding = resp.headers.getparam('charset')
        self.content_type = resp.headers.getheader('content-type')
        self.cookiejar = cookiejar

    @property
    def text(self):
        return resp.text

    @property
    def json(self):
        return resp.json()

    @property
    def xml(self):
        try:
            return xml.etree.ElementTree.parse(self.text)
        except xml.etree.ElementTree.ParseError:
            return None

class RequestException(Exception):
    pass
