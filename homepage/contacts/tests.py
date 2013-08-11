from __future__ import absolute_import

import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.test import TestCase
from django.test.client import Client

from .models import UserProfile


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('t1', 'a@aaa.com',
                                             password='123',
                                             first_name='fn',
                                             last_name='ln')
        self.profile = UserProfile(user=self.user)

    def test_proxied_properties(self):
        self.assertEqual(self.user.first_name, self.profile.first_name)
        self.assertEqual(self.user.last_name, self.profile.last_name)
        self.assertEqual(self.user.email, self.profile.email)

    def test_to_dict(self):
        data = self.profile.to_dict()
        required_fields = set(['first_name', 'last_name', 'date_of_birth',
                              'bio', 'email', 'jabber', 'skype',
                              'other_contacts'])
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
        required_fields = set(['first_name', 'last_name', 'date_of_birth',
                              'bio', 'email', 'jabber', 'skype',
                              'other_contacts'])
        self.assertEqual(set(json.loads(response.content).keys()),
                         required_fields)
