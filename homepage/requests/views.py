from __future__ import absolute_import

import json

from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import F
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.template import RequestContext

from .models import Request
from .forms import RequestVoteForm

RECENT_REQUESTS_COUNT = 10

def view_requests(request):
    if request.POST:
        vote_form = RequestVoteForm(request.POST)
        if vote_form.is_valid():
            req = Request.objects.filter(
                id=vote_form.cleaned_data['request_id'])
            req.update(priority=F('priority')+vote_form.cleaned_data['action'])
    requests =  Request.objects.all().order_by('created')
    requests = requests.order_by('-priority')
    return render_to_response('requests/no_js_index.html',
                              {'requests': requests[:RECENT_REQUESTS_COUNT]},
                              context_instance=RequestContext(request))

@require_http_methods(['GET'])
def get_requests(request, order_by_priority):
    order_by_priority = int(order_by_priority)

    requests = Request.objects.all().order_by('created')
    if order_by_priority:
        requests = requests.filter(priority=1).order_by('-priority')

    return HttpResponse(json.dumps({
        'data': [r.url for r in requests[:RECENT_REQUESTS_COUNT]]}),
        mimetype='application/json')
