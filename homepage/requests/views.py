from __future__ import absolute_import

import json

from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Request

@require_http_methods(['GET'])
def get_requests(request):
    requests = Request.objects.all().order_by('-created')[:10]
    return HttpResponse(json.dumps({'data': [r.url for r in requests]}),
                        mimetype='application/json')
