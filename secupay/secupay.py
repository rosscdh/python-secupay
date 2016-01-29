import re
import json
import requests
import urlparse

import logging
logger = logging.getLogger('secupay')

SUPPORTED_LANGUAGES = (('de_DE', 'Deutsch'), ('en_US', 'English'))


class Session(object):
    """
    Session object
    """
    site = 'https://api.secupay.ag/'
    token = None
    demo = "0"

    def __init__(self, token, **kwargs):
        self.token = token
        self.language = kwargs.pop('lang', 'en_US')

    @property
    def auth_url(self):
        return self.client.authorize_url(self.authorization_url,
                                         response_type=self.response_type)


class DevelopmentSession(Session):
    """
    Class to handle development test api requests.
    """
    site = 'https://api-dist.secupay-ag.de/'
    demo = "1"


class BaseApi(object):
    r = requests

    def __init__(self, session, **kwargs):
        self.session = session
        self.token = session.token
        self.response = self.response_json = {}
        self.params = kwargs

    @property
    def base_url(self):
        return self.session.site

    @property
    def status_code(self):
        return getattr(self.response, 'status_code', None)

    @property
    def ok(self):
        return getattr(self.response, 'ok', None)

    @property
    def parse_uri(self):
        uri = self.uri

        for k, v in self.params.iteritems():
            key = ':{key}'.format(key=k)
            uri = uri.replace(key, str(v))

        return re.sub(r'\/\:(\w)+', '', uri)

    def headers(self, **kwargs):
        headers = {'Content-Type': 'application/json; charset=utf-8;'}
        headers.update(kwargs)
        return headers

    def wrap_namespace(self, **kwargs):
        kwargs.update({
            'apikey': self.token,
            'demo': self.session.demo
        })
        return json.dumps({'data': kwargs})

    def endpoint(self, *args, **kwargs):
        return urlparse.urljoin(self.base_url, self.parse_uri, *args, **kwargs)

    def process(self, response):
        self.response = response
        if response.ok is True:
            self.response_json = self.response.json()
            return self.response_json
        #
        # Handle the bad CLI api implementation of 404 returning HTML and not
        # a valid REST reponse
        #
        return {'message': response.reason, 'ok': response.ok, 'status_code': response.status_code, 'url': response.url}

    def get(self, **kwargs):
        print self.endpoint()
        return self.process(response=self.r.get(self.endpoint(), headers=self.headers(), params=kwargs))

    def post(self, **kwargs):
        print self.wrap_namespace(**kwargs)
        return self.process(response=self.r.post(self.endpoint(), headers=self.headers(), data=self.wrap_namespace(**kwargs)))

    def put(self, **kwargs):
        return self.process(response=self.r.put(self.endpoint(), headers=self.headers(), data=self.wrap_namespace(**kwargs)))

    def patch(self, **kwargs):
        return self.process(response=self.r.patch(self.endpoint(), headers=self.headers(), data=self.wrap_namespace(**kwargs)))

    def delete(self, **kwargs):
        return self.process(response=self.r.delete(self.endpoint(), headers=self.headers(), params=kwargs))


class PaymentTypes(BaseApi):
    uri = 'payment/gettypes'

    def post(self, **kwargs):
        raise Exception('Not implemented for this %s' % self.__class__.__name__)

    def put(self, **kwargs):
        raise Exception('Not implemented for this %s' % self.__class__.__name__)

    def patch(self, **kwargs):
        raise Exception('Not implemented for this %s' % self.__class__.__name__)

    def delete(self, **kwargs):
        raise Exception('Not implemented for this %s' % self.__class__.__name__)


class Payment(BaseApi):
    uri = 'payment/init'

    class Status(BaseApi):
        uri = 'payment/status'

    def status(self):
        return self.Status(session=self.session)

    class CapturePreAuthorizedPayment(BaseApi):
        uri = 'payment/:hash/capture'

    def capture_preauthorized_payment(self, token):
        return self.CapturePreAuthorizedPayment(session=self.session,
                                                hash=token)

    class CancelPreAuthorizedPayment(BaseApi):
        uri = 'payment/:hash/cancel'

    def cancel_preauthorized_payment(self, token):
        return self.CancelPreAuthorizedPayment(session=self.session,
                                               hash=token)

    # class Invoice(BaseApi):
    #     uri = 'payment/:hash/cancel'


# class Documents(BaseApi):
#     uri = 'documents/:id'

#     def wrap_namespace(self, **kwargs):
#         return {'document': kwargs}

#     def document_versions(self):
#         return self.response_json.get('document', {}).get('document_versions', self.get().get('document', {}).get('document_versions',[]))

#     def download_version(self, version_id):
#         download = self.DownloadVersion(token=self.token, id=self.response_json.get('document', {}).get('id'), document_version=version_id)
#         return download.get()

#     class DownloadVersion(BaseApi):
#         uri = 'documents/:id/document_version/:document_version/download'

