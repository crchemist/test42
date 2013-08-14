from datetime import date
from json import dumps

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    skype = models.CharField(max_length=250)
    jabber = models.EmailField()
    other_contacts = models.TextField()

    date_of_birth = models.DateField()
    bio = models.TextField()

    photo = models.ImageField(null=True, blank=True, upload_to='images')

    @property
    def first_name(self):
        return self.user.first_name

    @first_name.setter
    def first_name(self, value):
        self.user.first_name = value

    @property
    def last_name(self):
        return self.user.last_name

    @last_name.setter
    def last_name(self, value):
        self.user.last_name = value

    @property
    def email(self):
        return self.user.email

    @email.setter
    def email(self, value):
        self.user.email = value

    def __unicode__(self):
        return self.user.email

    def to_dict(self, request=None):
        is_logged_in = False
        if request is not None:
            is_logged_in = request.user.is_authenticated()
        try:
            photo_url = self.photo.url
        except ValueError:
            photo_url = None

        user_ct = ContentType.objects.get_for_model(User)
        admin_url = reverse('admin:%s_%s_change' % (user_ct.app_label,
            user_ct.name), args=(self.id, ))

        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'bio': self.bio,
            'email': self.email,
            'jabber': self.jabber,
            'skype': self.skype,
            'other_contacts': self.other_contacts,
            'is_logged_in': is_logged_in,
            'photo_url': photo_url,
            'admin_url': admin_url}

    def jsonify(self, request=None):
        data = {}
        for key, value in self.to_dict(request).items():
            if isinstance(value, date):
                value = str(value)
            data[key] = value
        return dumps(data)

    def save_data(self, data, **kw):
        for key, value in data.items():
            setattr(self, key, value)
        self.user.save(**kw)
        self.save(**kw)
