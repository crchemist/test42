from django.conf.urls import patterns, url

urlpatterns = patterns('homepage.contacts.views',
    (r'^$', 'get_user_data'),
)
