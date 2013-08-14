from __future__ import absolute_import

import json
import os

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods

from .models import UserProfile
from .forms import ContactForm


def json_response(data, status=200):
    return HttpResponse(data, mimetype='application/json', status=status)


def index(request):
    return HttpResponseRedirect(settings.STATIC_URL + 'index.html')


@require_http_methods(['GET'])
def get_user_data(request):
    profile = UserProfile.objects.get()
    return json_response(profile.jsonify(request))


@login_required
@require_http_methods(['POST'])
def user_data_update(request):
    form = ContactForm(request.POST, request.FILES)
    result_data = {}
    if form.is_valid():
        UserProfile.objects.get().save_data(form.cleaned_data)
    else:
        result_data['errors'] = form.errors
    return json_response(json.dumps(result_data))


@require_http_methods(['POST'])
def user_login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        profile = UserProfile.objects.get()
        return json_response(profile.jsonify(request))
    return json_response(json.dumps({}), status=401)


@login_required
@require_http_methods(['GET'])
def user_logout(request):
    logout(request)
    return json_response(json.dumps({'is_logged_in': False}))
