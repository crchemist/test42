from __future__ import absolute_import

import json
import re
from StringIO import StringIO

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.handlers.wsgi import WSGIRequest

from django.test import TestCase
from django.test.client import Client

from .models import Request
from .middleware import RequestsStoreMiddleware


class RequestsMiddlewareTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        Request.objects.all().delete()

    def test_middleware(self):
        c = Client()
        self.assertEqual(Request.objects.all().count(), 0)

        c.get('/some_url')
        self.assertEqual(Request.objects.all().count(), 1)

    def test_requests_midleware_class(self):
        requests_middleware = RequestsStoreMiddleware()
        path = '/test-url2'
        req = WSGIRequest({'REQUEST_METHOD': 'GET',
                           'PATH_INFO': path,
                           'wsgi.input': StringIO()})
        requests_middleware.process_request(req)
        self.assertEqual(Request.objects.filter(url=path).count(), 1)

    def test_priority_requests(self):
        settings.PRIORITY_REQUESTS_PATT = re.compile(r'/test')
        requests_middleware = RequestsStoreMiddleware()
        path = '/test-url2'
        req = WSGIRequest({'REQUEST_METHOD': 'GET',
                           'PATH_INFO': path,
                           'wsgi.input': StringIO()})
        requests_middleware.process_request(req)
        self.assertEqual(Request.objects.filter(url=path).get().priority, 1)

        path = '/1test-url2'
        req = WSGIRequest({'REQUEST_METHOD': 'GET',
                           'PATH_INFO': path,
                           'wsgi.input': StringIO()})
        requests_middleware.process_request(req)
        self.assertEqual(Request.objects.filter(url=path).get().priority, 0)

    def test_get_requests(self):
        c = Client()

        response = c.get(reverse('requests_data'))
        data = json.loads(response.content)['data']
        self.assertTrue(reverse('requests_data') in data)
