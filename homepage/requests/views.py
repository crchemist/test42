from __future__ import absolute_import

import json

from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Request

RECENT_REQUESTS_COUNT = 10

@require_http_methods(['GET'])
def get_requests(request, order_by_priority):
    order_by_priority = int(order_by_priority)

    requests = Request.objects.all().order_by('created')
    if order_by_priority:
        requests = requests.filter(priority=1).order_by('-priority')

    return HttpResponse(json.dumps({
        'data': [r.url for r in requests[:RECENT_REQUESTS_COUNT]]}),
        mimetype='application/json')
