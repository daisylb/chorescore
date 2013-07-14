from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_name.views.home', name='home'),
    url(r'^$', chore_list, name='chore_list'),
    url(r'done/(?P<chore_id>\d+)', mark_chore_done, name='mark_done'),
    url(r'scores/$', scoreboard, name='scoreboard'),
)
