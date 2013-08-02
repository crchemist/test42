from __future__ import absolute_import

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import UserProfile

@require_http_methods(['GET'])
def get_user_data(request):
    user = UserProfile.objects.get()
    return HttpResponse(user.jsonify(), mimetype='application/json')
