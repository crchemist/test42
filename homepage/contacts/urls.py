from django.conf.urls import patterns, url

urlpatterns = patterns('homepage.contacts.views',
    url(r'^$', 'get_user_data', name='user_data'),
    url(r'update/$', 'user_data_update', name='user_data_update'),
    url(r'login/$', 'user_login', name='user_login'),
    url(r'logout/$', 'user_logout', name='user_logout'),
)
