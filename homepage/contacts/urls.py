from django.conf.urls import patterns, url

urlpatterns = patterns('homepage.contacts.views',
    url(r'^$', 'get_user_data', name='user_data'),
    url(r'login/$', 'user_login', name='user_login'),
)
