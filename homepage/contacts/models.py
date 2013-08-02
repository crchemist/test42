from datetime import date
from json import dumps

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    jabber = models.EmailField()
    skype = models.CharField(max_length=250)
    other_contacts = models.TextField()

    date_of_birth = models.DateField()
    bio = models.TextField()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name 

    @property
    def email(self):
        return self.user.email

    def __unicode__(self):
        return self.user.email

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'bio': self.bio,
            'email': self.email,
            'jabber': self.jabber,
            'skype': self.skype,
            'other_contacts': self.other_contacts}

    def jsonify(self):
        data = {}
        for key, value in self.to_dict().items():
            if isinstance(value, date):
                value = str(value)
            data[key] = value
        return dumps(data)
