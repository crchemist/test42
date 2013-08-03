from __future__ import absolute_import

import json
from StringIO import StringIO

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from django.test import TestCase
from django.test.client import Client

from .context_processors import django_settings
from .models import UserProfile

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('t1', 'a@aaa.com',
            password='123', first_name='fn', last_name='ln')
        self.profile = UserProfile(user=self.user)

    def test_proxied_properties(self):
        self.assertEqual(self.user.first_name, self.profile.first_name)
        self.assertEqual(self.user.last_name, self.profile.last_name)
        self.assertEqual(self.user.email, self.profile.email)

    def test_to_dict(self):
        data = self.profile.to_dict()
        required_fields = set(['first_name', 'last_name', 'date_of_birth',
            'bio', 'email', 'jabber', 'skype', 'other_contacts', 'is_logged_in'])
        available_fields = set(data.keys())

        self.assertTrue(isinstance(data, dict))
        self.assertEqual(available_fields, required_fields)

    def test_jsonify(self):
        data_str = self.profile.jsonify()
        self.assertTrue(isinstance(data_str, str))

        self.assertTrue(isinstance(json.loads(data_str), dict))


    def tearDown(self):
        UserProfile.objects.filter().delete()
        User.objects.filter().delete()


class ViewsTest(TestCase):
    def test_get_user_data(self):
        c = Client()
        response = c.get(reverse('user_data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'application/json')

    def test_settings_context_processor(self):
        processors = settings.TEMPLATE_CONTEXT_PROCESSORS
        self.assertTrue('homepage.contacts.context_processors.django_settings'
                        in processors)

        fake_request =  req = WSGIRequest({'REQUEST_METHOD': 'GET',
                                           'PATH_INFO': '/',
                                           'wsgi.input': StringIO()})
        self.assertTrue('django_settings' in django_settings(fake_request))
