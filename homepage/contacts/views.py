import json

from django.contrib.auth.models import User
from django.http import HttpResponse

def home(request):
    return HttpResponse(json.dumps({'users': [1,2]}), mimetype='application/json')
