from __future__ import absolute_import

from .models import Request

class RequestsStoreMiddleware(object):
    """Save path of each request to database
    """
    def process_request(self, request):
        """Record request to database
        """
        entry = Request(url=request.path)
        entry.save()
