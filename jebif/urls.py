# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from bioinfuse import views as bviews
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

ROOT = settings.ROOT_URL

BROOT = "%sbioinfuse/" % ROOT

urlpatterns = [
    # Administration
    url(r'^%sadmin/' % ROOT, include(admin.site.urls)),
    # Member login & logout
    url(r'^%slogin/$' % ROOT, auth_views.login, name="login"),
    url(r'^%saccounts/logout/$' % ROOT, auth_views.logout, {'next_page': '/%s'%BROOT}, name="logout"),
    url(r'^%saccounts/password/reset/$' % ROOT, password_reset, {'post_reset_redirect': '/%saccounts/password/done/' % ROOT}, name='password_reset'),
    url(r'^%saccounts/password/done/$' % ROOT, password_reset_done, name='password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', password_reset_confirm, {'post_reset_redirect' : '/%saccounts/password/done/' % ROOT}, name='password_reset_confirm'),
    url(r'^user/password/done/$', password_reset_complete, name='password_reset_complete'),
    # Home
    url(r'^%s$' % ROOT, bviews.home, name="home"),
    # BioInfuse
    url(r'%s' % BROOT, include('bioinfuse.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
