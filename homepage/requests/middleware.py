from __future__ import absolute_import

from django.conf import settings

from .models import Request


class RequestsStoreMiddleware(object):
    """Save path of each request to database
    """
    def process_request(self, request):
        """Record request to database
        """
        path = request.path
        entry = Request(url=path)
        if settings.PRIORITY_REQUESTS_PATT.match(path):
            entry.priority = 1
        entry.save()
