from django.conf.urls import patterns, url

urlpatterns = patterns('homepage.requests.views',
    url(r'^$', 'get_requests', name='requests_data'),
)
