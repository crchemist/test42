from __future__ import absolute_import

import json

from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test.client import Client

from .models import Request

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

    def test_get_requests(self):
        c = Client()

        response = c.get(reverse('requests_data'))
        data = json.loads(response.content)['data']
        self.assertTrue(reverse('requests_data') in data)
