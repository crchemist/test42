from __future__ import absolute_import

import os

from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods

from .models import UserProfile


def index(request):
    return HttpResponseRedirect(settings.STATIC_URL + 'index.html')


@require_http_methods(['GET'])
def get_user_data(request):
    user = UserProfile.objects.get()
    return HttpResponse(user.jsonify(), mimetype='application/json')
