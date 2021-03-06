from datetime import date
from json import dumps

from django.db import models, DatabaseError
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.db.models import signals
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
        if data.get('photo') is None:
            data = data.copy()
            data.pop('photo', None)
        for key, value in data.items():
            setattr(self, key, value)
        self.user.save(**kw)
        self.save(**kw)


class LogModelModification(models.Model):
    """Store information about models modifications.
    """
    action_time = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        """Metaclass for creating LogModelModification class
        """
        verbose_name = 'log entry'
        ordering = ('-action_time',)

    def __unicode__(self):
        """Represent entry in django.contib.admin and other places
        """
        action_str = 'Unknown action'
        if self.action_flag == ADDITION:
            action_str = 'Added'
        elif self.action_flag == CHANGE:
            action_str = 'Changed'
        elif self.action_flag == DELETION:
            action_str = 'Deleted'
        return '%s: %s' % (action_str, self.object_repr)


def log_modify(sender, instance, created, **kwargs):
    """Create LogModelModification entry each time
    any model is modified.
    """
    if sender is LogModelModification:
        return

    obj_ct = ContentType.objects.get_for_model(sender)
    obj_id = instance.pk
    action_flag = ADDITION if created else CHANGE
    try:
        LogModelModification.objects.create(content_type=obj_ct,
                          object_id=obj_id,
                          object_repr=repr(instance),
                          action_flag=action_flag)
    except DatabaseError:
        # db not yet synced
        pass


def log_delete(sender, instance, **kwargs):
    """Create LogModelModification entry each time
    any entry is deleted.
    """
    if sender is LogModelModification:
        return

    obj_ct = ContentType.objects.get_for_model(sender)
    obj_id = instance.id if hasattr(instance, 'id') else None
    LogModelModification.objects.create(content_type=obj_ct,
                          object_id=obj_id,
                          object_repr=repr(instance),
                          action_flag=DELETION)


signals.post_save.connect(log_modify, dispatch_uid='contacts.post_save')
signals.post_delete.connect(log_delete, dispatch_uid='contacts.post_delete')
