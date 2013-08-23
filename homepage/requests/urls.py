from django.conf.urls import patterns, url

urlpatterns = patterns('homepage.requests.views',
    url(r'^(\d)/$', 'get_requests', name='requests_data'),
)
