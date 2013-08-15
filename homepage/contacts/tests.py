from __future__ import absolute_import

import json
from datetime import date
from StringIO import StringIO

from django.core.urlresolvers import reverse
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.auth.models import User
from django.core.management import get_commands
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from django.test import TestCase
from django.test.client import Client

from .context_processors import django_settings
from .models import UserProfile, LogModelModification
from .management.commands.printmodels import Command
from .templatetags.edit_link import edit_link


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('t1', 'a@aaa.com',
                                             password='123',
                                             first_name='fn', last_name='ln')
        self.profile = UserProfile(user=self.user,
                                   date_of_birth=date(1987, 5, 22))
        self.profile.save()

    def test_user_login(self):
        c = Client()
        response = c.post(reverse('user_login'), json.dumps({
            'username': 't1',
            'password': '123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = c.post(reverse('user_login'), json.dumps({
            'username': 't1',
            'password': 'wrong'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_proxied_properties(self):
        self.assertEqual(self.user.first_name, self.profile.first_name)
        self.assertEqual(self.user.last_name, self.profile.last_name)
        self.assertEqual(self.user.email, self.profile.email)

    def test_edit_link_tag(self):
        """Test 'edit_link' tag
        """
        self.assertEqual(edit_link(self.user),
                  '/admin/auth/user/%s/' % self.user.id)

    def test_to_dict(self):
        data = self.profile.to_dict()
        required_fields = set(['first_name', 'photo_url',
            'last_name', 'date_of_birth', 'bio', 'email', 'jabber',
            'skype', 'other_contacts', 'is_logged_in', 'admin_url'])
        available_fields = set(data.keys())

        self.assertTrue(isinstance(data, dict))
        self.assertEqual(available_fields, required_fields)

    def test_jsonify(self):
        data_str = self.profile.jsonify()
        self.assertTrue(isinstance(data_str, str))

        self.assertTrue(isinstance(json.loads(data_str), dict))

    def test_save_data(self):
        self.profile.save_data({'first_name': 'SD'})
        self.assertEqual(self.profile.first_name, 'SD')
        self.assertEqual(self.profile.user.first_name, 'SD')

    def tearDown(self):
        UserProfile.objects.filter().delete()
        User.objects.filter().delete()


class ViewsTest(TestCase):
    fixtures = ['initial_data.json']

    def test_get_user_data(self):
        c = Client()
        response = c.get(reverse('user_data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'application/json')
        required_fields = set(['first_name', 'last_name', 'date_of_birth',
                              'bio', 'email', 'jabber', 'skype',
                              'other_contacts', 'photo_url', 'is_logged_in',
                              'admin_url'])
        self.assertEqual(set(json.loads(response.content).keys()),
                         required_fields)

    def test_settings_context_processor(self):
        processors = settings.TEMPLATE_CONTEXT_PROCESSORS
        self.assertTrue('homepage.contacts.context_processors.django_settings'
                        in processors)

        fake_request =  req = WSGIRequest({'REQUEST_METHOD': 'GET',
                                           'PATH_INFO': '/',
                                           'wsgi.input': StringIO()})
        self.assertTrue('django_settings' in django_settings(fake_request))

class ModificationLogTest(TestCase):
    def tearDownUp(self):
        LogModelModification.objects.all().delete()

    def test_modifications_log(self):
        """Test model modification logging facility
        """
        # for testing LogModelModification I will use UserProfile entry
        # test object creation
        user = User.objects.create_user('t1', 'a@aaa.com',
                                        password='123',
                                        first_name='fn', last_name='ln')
        profile = UserProfile(user=user,
                              date_of_birth=date(1987, 5, 22))
        profile.save()
        profile_ct = ContentType.objects.get_for_model(profile)

        log_entry = LogModelModification.objects.filter(
                     object_id=profile.id, content_type=profile_ct).get()

        self.assertEqual(log_entry.action_flag, ADDITION)

        # test object modification
        profile.first_name = 'other name'
        profile.save()

        log_entries = LogModelModification.objects.filter(
            object_id=profile.id, content_type=profile_ct)

        self.assertEqual(log_entries[0].action_flag, CHANGE)

        # test object removing
        profile.delete()
        log_entry = LogModelModification.objects.filter(
            object_id=profile.id, content_type=profile_ct)
        self.assertEqual(log_entries[0].action_flag, DELETION)

        log_entries_count = LogModelModification.objects.count()
        log_entry = LogModelModification.objects.all()[0]
        log_entry.delete()
        last_record = LogModelModification.objects.all()[0]
        self.assertNotEqual(last_record.content_type,
                ContentType.objects.get_for_model(LogModelModification))


class TestCommands(TestCase):

    def test_printmodels_command(self):
        """Test django-admin.py printmodels command
        """
        command = get_commands().get('printmodels')
        self.assertTrue(command)

    def test_printmodels_output(self):
        command = Command()
        command.stdout = StringIO()
        command.stderr = StringIO()
        command.handle()

        command.stdout.seek(0)
        command.stderr.seek(0)
        self.assertTrue('UserProfile' in command.stdout.read())
        self.assertTrue('UserProfile' in command.stderr.read())
