# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from bioinfuse import views as bviews
from django.conf import settings
from django.conf.urls.static import static

ROOT = settings.ROOT_URL

urlpatterns = [
    # Administration
    url(r'^%sadmin/' % ROOT, include(admin.site.urls)),
    # Home
    url(r'^a/$', bviews.index, name='index'),
    # Member
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/bioinfuse/'}),
    url(r'a/subscribe/$', bviews.subscribe, name='subscribe'),
    url(r'a/edit_profile/(?P<member>[0-9]+)', bviews.edit_profile, name='edit_profile'),
    url(r'a/manage_members', bviews.list_members, name="manage_members"),
    url(r'a/edit_member/(?P<member>[0-9]+)', bviews.edit_member, name="edit_member"),
    url(r'a/submit_movie/(?P<member>[0-9]+)$', bviews.submit_movie, name="submit_movie"),
]
